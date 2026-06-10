from fastapi import HTTPException

from app.models.channel import Channel
from app.models.channel_member import ChannelMember


def create_channel(db, data):

    channel = Channel(
        tenant_id=data.tenant_id,
        workspace_id=data.workspace_id,
        name=data.name,
        description=data.description,
        channel_type=data.channel_type,
        created_by=data.created_by
    )

    db.add(channel)
    db.commit()
    db.refresh(channel)

    return channel


def get_channels(db, workspace_id):

    return db.query(Channel).filter(
        Channel.workspace_id == workspace_id
    ).all()


def get_channel(db, channel_id):

    channel = db.query(Channel).filter(
        Channel.id == channel_id
    ).first()

    if not channel:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return channel


def update_channel(db, channel_id, data):

    channel = get_channel(db, channel_id)

    channel.name = data.name
    channel.description = data.description
    channel.channel_type = data.channel_type

    db.commit()
    db.refresh(channel)

    return channel


def archive_channel(db, channel_id):

    channel = get_channel(db, channel_id)

    channel.is_archived = True

    db.commit()

    return {"message": "Channel archived"}


def restore_channel(db, channel_id):

    channel = get_channel(db, channel_id)

    channel.is_archived = False

    db.commit()

    return {"message": "Channel restored"}


def join_channel(db, channel_id, user_id):

    existing = db.query(ChannelMember).filter(
        ChannelMember.channel_id == channel_id,
        ChannelMember.user_id == user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already joined"
        )

    member = ChannelMember(
        channel_id=channel_id,
        user_id=user_id
    )

    db.add(member)
    db.commit()

    return {"message": "Joined channel"}


def leave_channel(db, channel_id, user_id):

    member = db.query(ChannelMember).filter(
        ChannelMember.channel_id == channel_id,
        ChannelMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Membership not found"
        )

    db.delete(member)
    db.commit()

    return {"message": "Left channel"}