from datetime import datetime

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.channel_message import (
    ChannelMessage
)
from app.models.channel import Channel
from app.models.channel_member import ChannelMember


def create_channel_message(
    db: Session,
    data
):
    channel_stmt = (
        select(Channel)
        .where(
            Channel.id == data.channel_id,
            Channel.workspace_id == data.workspace_id,
            Channel.tenant_id == data.tenant_id,
            Channel.is_archived.is_(False)
        )
    )

    channel = db.execute(channel_stmt).scalar_one_or_none()

    if not channel:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    member_stmt = (
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == data.channel_id,
            ChannelMember.user_id == data.sender_id
        )
    )

    member = db.execute(member_stmt).scalar_one_or_none()

    if not member:
        if channel.created_by != data.sender_id:
            raise HTTPException(
                status_code=400,
                detail="User is not channel member"
            )

        member = ChannelMember(
            channel_id=data.channel_id,
            user_id=data.sender_id
        )

        db.add(member)
        db.flush()

    msg = ChannelMessage(
        tenant_id=data.tenant_id,
        workspace_id=data.workspace_id,
        channel_id=data.channel_id,
        sender_id=data.sender_id,
        content=data.content
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)

    return msg


def get_channel_messages(
    db: Session,
    channel_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None
):
    if tenant_id is not None:
        channel_stmt = (
            select(Channel)
            .where(
                Channel.id == channel_id,
                Channel.tenant_id == tenant_id,
                Channel.is_archived.is_(False)
            )
        )

        channel = db.execute(channel_stmt).scalar_one_or_none()

        if not channel:
            raise HTTPException(
                status_code=404,
                detail="Channel not found"
            )

        if user_id is not None:
            member_stmt = (
                select(ChannelMember)
                .where(
                    ChannelMember.channel_id == channel_id,
                    ChannelMember.user_id == user_id
                )
            )

            member = db.execute(member_stmt).scalar_one_or_none()

            if not member and channel.created_by != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="User is not channel member"
                )

    stmt = (
        select(ChannelMessage)
        .where(
            ChannelMessage.channel_id
            == channel_id,
            ChannelMessage.deleted_at.is_(None)
        )
        .order_by(
            ChannelMessage.created_at.desc()
        )
    )

    return paginate(
        db,
        stmt
    )


def update_channel_message(
    db: Session,
    message_id: int,
    data
):
    stmt = (
        select(ChannelMessage)
        .where(
            ChannelMessage.id
            == message_id
        )
    )

    msg = db.execute(
        stmt
    ).scalar_one_or_none()

    if not msg:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    msg.content = data.content
    msg.edited_at = datetime.utcnow()

    db.commit()
    db.refresh(msg)

    return msg


def delete_channel_message(
    db: Session,
    message_id: int
):
    stmt = (
        select(ChannelMessage)
        .where(
            ChannelMessage.id
            == message_id
        )
    )

    msg = db.execute(
        stmt
    ).scalar_one_or_none()

    if not msg:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    msg.deleted_at = datetime.utcnow()

    db.commit()

    return {
        "message":
        "Channel message deleted"
    }
