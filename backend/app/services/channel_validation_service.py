from sqlalchemy import select

from app.models.channel_member import (
    ChannelMember
)


def validate_channel_member(
    db,
    channel_id: int,
    user_id: int
):
    stmt = (
        select(ChannelMember)
        .where(
            ChannelMember.channel_id
            == channel_id,

            ChannelMember.user_id
            == user_id
        )
    )

    member = db.execute(
        stmt
    ).scalar_one_or_none()

    if member:
        return {
            "success": True,
            "message": "User belongs to channel"
        }

    return {
        "success": False,
        "message": "User is not channel member"
    }