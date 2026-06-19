from sqlalchemy import select

from app.models.workspace_member import (
    WorkspaceMember
)


def validate_workspace_member(
    db,
    workspace_id: int,
    user_id: int
):
    stmt = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id
            == workspace_id,

            WorkspaceMember.user_id
            == user_id
        )
    )

    member = db.execute(
        stmt
    ).scalar_one_or_none()

    if member:
        return {
            "success": True,
            "message": "User belongs to workspace"
        }

    return {
        "success": False,
        "message": "User is not workspace member"
    }