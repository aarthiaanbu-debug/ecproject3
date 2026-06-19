from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import HTTPException

from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.workspace_task import (
    WorkspaceTask
)

from app.models.workspace_member import (
    WorkspaceMember
)

from app.models.workspace import (
    Workspace
)

from app.models.user import (
    User
)


def normalize_due_date(value):
    if not value or isinstance(value, datetime):
        return value

    if isinstance(value, str):
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

    return value


def create_workspace_task(
    db: Session,
    data
):
    workspace_stmt = (
        select(Workspace)
        .where(
            Workspace.id == data.workspace_id,
            Workspace.tenant_id == data.tenant_id,
            Workspace.is_archived.is_(False)
        )
    )

    workspace = db.execute(
        workspace_stmt
    ).scalar_one_or_none()

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    creator_stmt = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id == data.workspace_id,
            WorkspaceMember.user_id == data.created_by,
            WorkspaceMember.is_active.is_(True)
        )
    )

    creator_member = db.execute(
        creator_stmt
    ).scalar_one_or_none()

    if not creator_member:
        creator_user_stmt = (
            select(User)
            .where(
                User.id == data.created_by
            )
        )

        creator_user = db.execute(
            creator_user_stmt
        ).scalar_one_or_none()

        if not creator_user:
            raise HTTPException(
                status_code=404,
                detail="Task creator not found"
            )

        if (
            creator_user.organization_id is not None
            and creator_user.organization_id != data.tenant_id
        ):
            raise HTTPException(
                status_code=403,
                detail="Cross tenant access denied"
            )

        creator_member = WorkspaceMember(
            workspace_id=data.workspace_id,
            user_id=data.created_by,
            role="Owner" if workspace.created_by == data.created_by else "Member",
            is_active=True
        )

        db.add(creator_member)
        db.flush()

    if data.assigned_to is not None:
        user_stmt = (
            select(User)
            .where(
                User.id == data.assigned_to
            )
        )

        assigned_user = db.execute(
            user_stmt
        ).scalar_one_or_none()

        if not assigned_user:
            raise HTTPException(
                status_code=404,
                detail="Assigned user not found"
            )

        member_stmt = (
            select(WorkspaceMember)
            .where(
                WorkspaceMember.workspace_id == data.workspace_id,
                WorkspaceMember.user_id == data.assigned_to,
                WorkspaceMember.is_active.is_(True)
            )
        )

        assigned_member = db.execute(
            member_stmt
        ).scalar_one_or_none()

        if not assigned_member:
            raise HTTPException(
                status_code=400,
                detail="User is not workspace member"
            )

    task = WorkspaceTask(
        tenant_id=data.tenant_id,
        workspace_id=data.workspace_id,
        title=data.title,
        description=data.description,
        assigned_to=data.assigned_to,
        priority=data.priority,
        due_date=normalize_due_date(data.due_date),
        created_by=data.created_by
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_workspace_tasks(
    db: Session,
    workspace_id: int
):
    stmt = (
        select(WorkspaceTask)
        .where(
            WorkspaceTask.workspace_id
            == workspace_id
        )
    )

    return paginate(
        db,
        stmt
    )


def get_workspace_task(
    db: Session,
    task_id: int
):
    stmt = (
        select(WorkspaceTask)
        .where(
            WorkspaceTask.id == task_id
        )
    )

    return db.execute(
        stmt
    ).scalar_one_or_none()
