from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.database import get_db

from app.schemas.role_permission_schema import (
    RolePermissionCreate,
    RolePermissionUpdate,
    RolePermissionResponse
)

from app.services.role_permission_service import (
    create_permission,
    get_permissions,
    get_permission,
    update_permission,
    delete_permission
)

router = APIRouter(
    prefix="/role-permissions",
    tags=["RBAC"]
)


@router.post(
    "",
    response_model=RolePermissionResponse
)
def create(
    data: RolePermissionCreate,
    db: Session = Depends(get_db)
):
    return create_permission(
        db,
        data
    )


@router.get(
    "",
    response_model=Page[
        RolePermissionResponse
    ]
)
def list_permissions(
    db: Session = Depends(get_db)
):
    return get_permissions(
        db
    )


@router.get(
    "/{permission_id}",
    response_model=RolePermissionResponse
)
def get_one(
    permission_id: int,
    db: Session = Depends(get_db)
):
    return get_permission(
        db,
        permission_id
    )


@router.put(
    "/{permission_id}",
    response_model=RolePermissionResponse
)
def update(
    permission_id: int,
    data: RolePermissionUpdate,
    db: Session = Depends(get_db)
):
    return update_permission(
        db,
        permission_id,
        data
    )


@router.delete(
    "/{permission_id}"
)
def delete(
    permission_id: int,
    db: Session = Depends(get_db)
):
    return delete_permission(
        db,
        permission_id
    )