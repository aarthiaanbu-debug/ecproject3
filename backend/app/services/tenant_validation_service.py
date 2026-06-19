from sqlalchemy import select

from app.models.workspace import Workspace
from app.models.channel import Channel


def validate_workspace_tenant(
    db,
    workspace_id: int,
    tenant_id: int
):
    stmt = (
        select(Workspace)
        .where(
            Workspace.id
            == workspace_id
        )
    )

    workspace = db.execute(
        stmt
    ).scalar_one_or_none()

    if not workspace:
        return {
            "success": False,
            "message": "Workspace not found"
        }

    if workspace.tenant_id != tenant_id:
        return {
            "success": False,
            "message": "Cross tenant access denied"
        }

    return {
        "success": True,
        "message": "Tenant validated"
    }


def validate_channel_tenant(
    db,
    channel_id: int,
    tenant_id: int
):
    stmt = (
        select(Channel)
        .where(
            Channel.id
            == channel_id
        )
    )

    channel = db.execute(
        stmt
    ).scalar_one_or_none()

    if not channel:
        return {
            "success": False,
            "message": "Channel not found"
        }

    if channel.tenant_id != tenant_id:
        return {
            "success": False,
            "message": "Cross tenant access denied"
        }

    return {
        "success": True,
        "message": "Tenant validated"
    }