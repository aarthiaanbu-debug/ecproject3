from sqlalchemy import select
from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.workspace_message import (
    WorkspaceMessage
)
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.models.user import User


def _is_admin(db, user_id: int) -> bool:
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()

    return bool(user and user.role == "admin")


def _get_workspace(db, workspace_id: int, tenant_id: int):
    stmt = (
        select(Workspace)
        .where(
            Workspace.id == workspace_id,
            Workspace.tenant_id == tenant_id,
            Workspace.is_archived.is_(False)
        )
    )

    workspace = db.execute(stmt).scalar_one_or_none()

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return workspace


def _ensure_workspace_member(
    db,
    workspace: Workspace,
    user_id: int
):
    member_stmt = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id == workspace.id,
            WorkspaceMember.user_id == user_id,
            WorkspaceMember.is_active.is_(True)
        )
    )

    member = db.execute(member_stmt).scalar_one_or_none()

    if member:
        return member

    if workspace.created_by != user_id:
        raise HTTPException(
            status_code=403,
            detail="User is not workspace member"
        )

    member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=user_id,
        role="Owner",
        is_active=True
    )

    db.add(member)
    db.flush()

    return member


def create_workspace_message(
    db,
    data
):
    if not data.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    workspace = _get_workspace(
        db,
        data.workspace_id,
        data.tenant_id
    )

    _ensure_workspace_member(
        db,
        workspace,
        data.user_id
    )

    message = WorkspaceMessage(
        tenant_id=data.tenant_id,
        workspace_id=data.workspace_id,
        user_id=data.user_id,
        message=data.message
    )

    db.add(message)

    db.commit()

    db.refresh(message)

    return message


def get_workspace_messages(
    db,
    workspace_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None
):
    if tenant_id is not None:
        workspace = _get_workspace(
            db,
            workspace_id,
            tenant_id
        )

        if user_id is not None:
            _ensure_workspace_member(
                db,
                workspace,
                user_id
            )

    stmt = (
        select(
            WorkspaceMessage
        )
        .where(
            WorkspaceMessage.workspace_id
            == workspace_id
        )
        .order_by(
            WorkspaceMessage.id.desc()
        )
    )

    return paginate(db, stmt)


def update_workspace_message(
    db,
    message_id: int,
    data
):
    if not data.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    stmt = (
        select(WorkspaceMessage)
        .where(
            WorkspaceMessage.id == message_id,
            WorkspaceMessage.tenant_id == data.tenant_id
        )
    )

    message = db.execute(stmt).scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=404,
            detail="Workspace message not found"
        )

    workspace = _get_workspace(
        db,
        message.workspace_id,
        data.tenant_id
    )

    _ensure_workspace_member(
        db,
        workspace,
        data.user_id
    )

    if message.user_id != data.user_id and not _is_admin(db, data.user_id):
        raise HTTPException(
            status_code=403,
            detail="Only sender or admin can edit this message"
        )

    message.message = data.message

    db.commit()
    db.refresh(message)

    return message


def delete_workspace_message(
    db,
    message_id: int,
    tenant_id: int,
    user_id: int
):
    stmt = (
        select(WorkspaceMessage)
        .where(
            WorkspaceMessage.id == message_id,
            WorkspaceMessage.tenant_id == tenant_id
        )
    )

    message = db.execute(stmt).scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=404,
            detail="Workspace message not found"
        )

    workspace = _get_workspace(
        db,
        message.workspace_id,
        tenant_id
    )

    _ensure_workspace_member(
        db,
        workspace,
        user_id
    )

    if message.user_id != user_id and not _is_admin(db, user_id):
        raise HTTPException(
            status_code=403,
            detail="Only sender or admin can delete this message"
        )

    db.delete(message)
    db.commit()

    return {
        "message": "Workspace message deleted"
    }
