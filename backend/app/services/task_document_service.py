from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.task_document import (
    TaskDocument
)
from app.models.workspace_task import WorkspaceTask
from app.models.workspace_member import WorkspaceMember
from app.models.user import User


def _is_admin(db: Session, user_id: int) -> bool:
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()

    return bool(user and user.role == "admin")


def _get_authorized_task(
    db: Session,
    task_id: int,
    tenant_id: int,
    user_id: int
):
    task_stmt = (
        select(WorkspaceTask)
        .where(
            WorkspaceTask.id == task_id,
            WorkspaceTask.tenant_id == tenant_id
        )
    )

    task = db.execute(task_stmt).scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if _is_admin(db, user_id):
        return task

    member_stmt = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id == task.workspace_id,
            WorkspaceMember.user_id == user_id,
            WorkspaceMember.is_active.is_(True)
        )
    )

    member = db.execute(member_stmt).scalar_one_or_none()

    if not member and task.created_by != user_id and task.assigned_to != user_id:
        raise HTTPException(
            status_code=403,
            detail="Document access denied"
        )

    return task

def upload_task_document(
    db,
    tenant_id,
    task_id,
    uploaded_by,
    file_name,
    file_path
):
    _get_authorized_task(
        db,
        task_id,
        tenant_id,
        uploaded_by
    )

    doc = TaskDocument(
        tenant_id=tenant_id,
        task_id=task_id,
        uploaded_by=uploaded_by,
        file_name=file_name,
        file_path=file_path
    )

    db.add(doc)

    db.commit()

    db.refresh(doc)

    return doc


def get_task_documents(
    db: Session,
    task_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None
):
    if tenant_id is not None and user_id is not None:
        _get_authorized_task(
            db,
            task_id,
            tenant_id,
            user_id
        )

    stmt = (
        select(TaskDocument)
        .where(
            TaskDocument.task_id
            == task_id
        )
    )

    return paginate(
        db,
        stmt
    )


def delete_task_document(
    db: Session,
    document_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None
):
    stmt = (
        select(TaskDocument)
        .where(
            TaskDocument.id
            == document_id
        )
    )

    doc = db.execute(
        stmt
    ).scalar_one_or_none()

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Task document not found"
        )

    if tenant_id is not None and user_id is not None:
        _get_authorized_task(
            db,
            doc.task_id,
            tenant_id,
            user_id
        )

    db.delete(doc)
    db.commit()

    return {
        "message":
        "Task document deleted"
    }


def get_task_document_for_download(
    db: Session,
    document_id: int,
    tenant_id: int,
    user_id: int
):
    stmt = (
        select(TaskDocument)
        .where(
            TaskDocument.id == document_id,
            TaskDocument.tenant_id == tenant_id
        )
    )

    doc = db.execute(stmt).scalar_one_or_none()

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Task document not found"
        )

    _get_authorized_task(
        db,
        doc.task_id,
        tenant_id,
        user_id
    )

    return doc
