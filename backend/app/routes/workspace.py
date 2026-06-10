from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.workspace_schema import (
    WorkspaceCreate,
    WorkspaceUpdate
)

from app.services.workspace_service import (
    create_workspace,
    get_workspaces,
    get_workspace,
    update_workspace,
    archive_workspace,
    restore_workspace
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace"]
)


@router.post("")
def create(data: WorkspaceCreate,
           db: Session = Depends(get_db)):
    return create_workspace(db, data)


@router.get("")
def list_all(
    db: Session = Depends(get_db)
):
    return get_workspaces(db)


@router.get("/{workspace_id}")
def get_one(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    return get_workspace(db, workspace_id)


@router.put("/{workspace_id}")
def update(
    workspace_id: int,
    data: WorkspaceUpdate,
    db: Session = Depends(get_db)
):
    return update_workspace(
        db,
        workspace_id,
        data
    )


@router.patch("/{workspace_id}/archive")
def archive(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    return archive_workspace(
        db,
        workspace_id
    )


@router.patch("/{workspace_id}/restore")
def restore(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    return restore_workspace(
        db,
        workspace_id
    )