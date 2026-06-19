from fastapi import HTTPException
from sqlalchemy import select

from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.models.user import User


def create_workspace(db, data):

    existing_stmt = (
        select(Workspace)
        .where(
            Workspace.slug == data.slug
        )
    )

    existing = db.execute(
        existing_stmt
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Workspace slug already exists"
        )

    workspace = Workspace(
        tenant_id=data.tenant_id,
        name=data.name,
        slug=data.slug,
        description=data.description,
        avatar_url=data.avatar_url,
        visibility=data.visibility,
        created_by=data.created_by
    )

    db.add(workspace)
    db.flush()

    creator_member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=data.created_by,
        role="Owner",
        is_active=True
    )

    db.add(creator_member)
    db.commit()
    db.refresh(workspace)

    return workspace


def get_workspaces(db):
    stmt = select(Workspace)

    return db.execute(
        stmt
    ).scalars().all()


def get_workspace(db, workspace_id):

    stmt = (
        select(Workspace)
        .where(
            Workspace.id == workspace_id
        )
    )

    workspace = db.execute(
        stmt
    ).scalar_one_or_none()

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return workspace


def update_workspace(db, workspace_id, data):

    workspace = get_workspace(db, workspace_id)

    workspace.name = data.name
    workspace.description = data.description
    workspace.visibility = data.visibility

    db.commit()
    db.refresh(workspace)

    return workspace


def archive_workspace(db, workspace_id):

    workspace = get_workspace(db, workspace_id)

    workspace.is_archived = True

    db.commit()

    return {"message": "Workspace archived"}


def restore_workspace(db, workspace_id):

    workspace = get_workspace(db, workspace_id)

    workspace.is_archived = False

    db.commit()

    return {"message": "Workspace restored"}


def get_workspace_members(db, workspace_id):
    get_workspace(db, workspace_id)

    stmt = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.is_active.is_(True)
        )
    )

    return db.execute(
        stmt
    ).scalars().all()


def add_workspace_member(db, workspace_id, data):
    workspace = get_workspace(db, workspace_id)
    user_id = data.get("user_id")
    role = data.get("role", "Member")

    user_stmt = select(User).where(User.id == user_id)
    user = db.execute(user_stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.organization_id is not None and user.organization_id != workspace.tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Cross tenant access denied"
        )

    existing_stmt = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id
        )
    )

    existing = db.execute(
        existing_stmt
    ).scalar_one_or_none()

    if existing:
        existing.role = role
        existing.is_active = True
        db.commit()
        db.refresh(existing)
        return existing

    member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=user_id,
        role=role,
        is_active=True
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


def update_workspace_member_role(db, workspace_id, user_id, role):
    stmt = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id
        )
    )

    member = db.execute(stmt).scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Workspace membership not found"
        )

    member.role = role
    member.is_active = True
    db.commit()
    db.refresh(member)

    return member


def remove_workspace_member(db, workspace_id, user_id):
    stmt = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id
        )
    )

    member = db.execute(stmt).scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Workspace membership not found"
        )

    member.is_active = False
    db.commit()

    return {
        "message": "Workspace member removed"
    }
