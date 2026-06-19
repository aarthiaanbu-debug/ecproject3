from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.workspace_message_schema import (
    WorkspaceMessageCreate,
    WorkspaceMessageUpdate,
    WorkspaceMessageResponse
)

from app.services.workspace_message_service import (
    create_workspace_message,
    get_workspace_messages,
    update_workspace_message,
    delete_workspace_message
)

from fastapi_pagination import (
    Page
)

router = APIRouter(
    prefix="/workspace-messages",
    tags=["Workspace Messages"]
)


@router.post(
    "",
    response_model=WorkspaceMessageResponse
)
def create_message(
    data: WorkspaceMessageCreate,
    db: Session = Depends(get_db)
):

    return create_workspace_message(
        db,
        data
    )


@router.get(
    "/{workspace_id}",
    response_model=Page[
        WorkspaceMessageResponse
    ]
)
def get_messages(
    workspace_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_workspace_messages(
        db,
        workspace_id,
        tenant_id,
        user_id
    )


@router.put(
    "/{message_id}",
    response_model=WorkspaceMessageResponse
)
def update_message(
    message_id: int,
    data: WorkspaceMessageUpdate,
    db: Session = Depends(get_db)
):
    return update_workspace_message(
        db,
        message_id,
        data
    )


@router.delete(
    "/{message_id}"
)
def delete_message(
    message_id: int,
    tenant_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    return delete_workspace_message(
        db,
        message_id,
        tenant_id,
        user_id
    )
