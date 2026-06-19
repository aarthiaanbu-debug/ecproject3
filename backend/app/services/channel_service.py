from fastapi import HTTPException
from sqlalchemy import select

from app.models.channel import Channel
from app.models.channel_member import ChannelMember
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember


def create_channel(db, data):
    workspace_stmt = (
        select(Workspace)
        .where(
            Workspace.id == data.workspace_id,
            Workspace.tenant_id == data.tenant_id,
            Workspace.is_archived.is_(False)
        )
    )

    workspace = db.execute(workspace_stmt).scalar_one_or_none()

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    member_stmt = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id == data.workspace_id,
            WorkspaceMember.user_id == data.created_by,
            WorkspaceMember.is_active.is_(True)
        )
    )

    member = db.execute(member_stmt).scalar_one_or_none()

    if not member:
        if workspace.created_by != data.created_by:
            raise HTTPException(
                status_code=400,
                detail="User is not workspace member"
            )

        member = WorkspaceMember(
            workspace_id=data.workspace_id,
            user_id=data.created_by,
            role="Owner",
            is_active=True
        )

        db.add(member)
        db.flush()

    channel = Channel(
        tenant_id=data.tenant_id,
        workspace_id=data.workspace_id,
        name=data.name,
        description=data.description,
        channel_type=data.channel_type,
        created_by=data.created_by
    )

    db.add(channel)
    db.flush()

    creator_member = ChannelMember(
        channel_id=channel.id,
        user_id=data.created_by
    )

    db.add(creator_member)
    db.commit()
    db.refresh(channel)

    return channel


def get_channels(db, workspace_id):

    stmt = (
        select(Channel)
        .where(
            Channel.workspace_id == workspace_id,
            Channel.is_archived.is_(False)
        )
    )

    return db.execute(
        stmt
    ).scalars().all()


def get_channel(db, channel_id):

    stmt = (
        select(Channel)
        .where(
            Channel.id == channel_id
        )
    )

    channel = db.execute(
        stmt
    ).scalar_one_or_none()

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

    existing_stmt = (
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id
        )
    )

    existing = db.execute(
        existing_stmt
    ).scalar_one_or_none()

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

    member_stmt = (
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id
        )
    )

    member = db.execute(
        member_stmt
    ).scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Membership not found"
        )

    db.delete(member)
    db.commit()

    return {"message": "Left channel"}
