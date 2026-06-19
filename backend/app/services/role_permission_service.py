from sqlalchemy import select

from fastapi import HTTPException

from fastapi_pagination.ext.sqlalchemy import (
    paginate
)

from app.models.role_permission import (
    RolePermission
)


def create_permission(
    db,
    data
):
    permission = RolePermission(
        role_name=data.role_name,
        module_name=data.module_name,

        can_create=data.can_create,
        can_read=data.can_read,
        can_update=data.can_update,
        can_delete=data.can_delete
    )

    db.add(permission)

    db.commit()

    db.refresh(permission)

    return permission


def get_permissions(
    db
):
    stmt = select(
        RolePermission
    )

    return paginate(
        db,
        stmt
    )


def get_permission(
    db,
    permission_id
):
    stmt = (
        select(RolePermission)
        .where(
            RolePermission.id
            == permission_id
        )
    )

    permission = db.execute(
        stmt
    ).scalar_one_or_none()

    if not permission:
        raise HTTPException(
            status_code=404,
            detail="Permission not found"
        )

    return permission


def update_permission(
    db,
    permission_id,
    data
):
    permission = get_permission(
        db,
        permission_id
    )

    permission.can_create = data.can_create
    permission.can_read = data.can_read
    permission.can_update = data.can_update
    permission.can_delete = data.can_delete

    db.commit()

    db.refresh(permission)

    return permission


def delete_permission(
    db,
    permission_id
):
    permission = get_permission(
        db,
        permission_id
    )

    db.delete(permission)

    db.commit()

    return {
        "message":
        "Permission deleted"
    }