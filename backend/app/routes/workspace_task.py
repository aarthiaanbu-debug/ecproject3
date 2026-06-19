from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.database import get_db

from app.schemas.workspace_task_schema import (
    WorkspaceTaskCreate,
    WorkspaceTaskResponse
)

from app.services.workspace_task_service import (
    create_workspace_task,
    get_workspace_tasks,
    get_workspace_task
)

router = APIRouter(
    prefix="/workspace-tasks",
    tags=["Workspace Tasks"]
)


@router.post(
    "",
    response_model=WorkspaceTaskResponse
)
def create(
    data: WorkspaceTaskCreate,
    db: Session = Depends(get_db)
):
    return create_workspace_task(
        db,
        data
    )


@router.get(
    "/workspace/{workspace_id}",
    response_model=Page[
        WorkspaceTaskResponse
    ]
)
def list_tasks(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    return get_workspace_tasks(
        db,
        workspace_id
    )


@router.get(
    "/{task_id}",
    response_model=WorkspaceTaskResponse
)
def get_one(
    task_id: int,
    db: Session = Depends(get_db)
):
    return get_workspace_task(
        db,
        task_id
    )