from fastapi import HTTPException
from app.models.workspace import Workspace


def create_workspace(db, data):

    existing = db.query(Workspace).filter(
        Workspace.slug == data.slug
    ).first()

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
    db.commit()
    db.refresh(workspace)

    return workspace


def get_workspaces(db):
    return db.query(Workspace).all()


def get_workspace(db, workspace_id):

    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()

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