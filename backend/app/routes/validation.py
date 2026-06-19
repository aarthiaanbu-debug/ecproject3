from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.services.workspace_validation_service import (
    validate_workspace_member
)

from app.services.channel_validation_service import (
    validate_channel_member
)

from app.services.tenant_validation_service import (
    validate_workspace_tenant,
    validate_channel_tenant
)

router = APIRouter(
    prefix="/validation",
    tags=["Validation"]
)


@router.get(
    "/workspace/{workspace_id}/user/{user_id}"
)
def workspace_validation(
    workspace_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    return validate_workspace_member(
        db,
        workspace_id,
        user_id
    )


@router.get(
    "/channel/{channel_id}/user/{user_id}"
)
def channel_validation(
    channel_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    return validate_channel_member(
        db,
        channel_id,
        user_id
    )


@router.get(
    "/workspace/{workspace_id}/tenant/{tenant_id}"
)
def workspace_tenant_validation(
    workspace_id: int,
    tenant_id: int,
    db: Session = Depends(get_db)
):
    return validate_workspace_tenant(
        db,
        workspace_id,
        tenant_id
    )


@router.get(
    "/channel/{channel_id}/tenant/{tenant_id}"
)
def channel_tenant_validation(
    channel_id: int,
    tenant_id: int,
    db: Session = Depends(get_db)
):
    return validate_channel_tenant(
        db,
        channel_id,
        tenant_id
    )