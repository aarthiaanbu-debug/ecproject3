from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.channel_task import ChannelTask
from app.models.channel_member import ChannelMember
from app.models.channel import Channel
from app.models.user import User


def create_channel_task(
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

    channel = db.execute(
        channel_stmt
    ).scalar_one_or_none()

    if not channel:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    creator_stmt = (
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == data.channel_id,
            ChannelMember.user_id == data.created_by
        )
    )

    creator_member = db.execute(
        creator_stmt
    ).scalar_one_or_none()

    if not creator_member:
        if channel.created_by != data.created_by:
            raise HTTPException(
                status_code=400,
                detail="Task creator is not channel member"
            )

        creator_member = ChannelMember(
            channel_id=data.channel_id,
            user_id=data.created_by
        )

        db.add(creator_member)
        db.flush()

    if data.assigned_to is not None:
        user_stmt = (
            select(User)
            .where(
                User.id == data.assigned_to
            )
        )

        assigned_user = db.execute(
            user_stmt
        ).scalar_one_or_none()

        if not assigned_user:
            raise HTTPException(
                status_code=404,
                detail="Assigned user not found"
            )

        member_stmt = (
            select(ChannelMember)
            .where(
                ChannelMember.channel_id == data.channel_id,
                ChannelMember.user_id == data.assigned_to
            )
        )

        assigned_member = db.execute(
            member_stmt
        ).scalar_one_or_none()

        if not assigned_member:
            raise HTTPException(
                status_code=400,
                detail="User is not channel member"
            )

    task = ChannelTask(
        tenant_id=data.tenant_id,
        workspace_id=data.workspace_id,
        channel_id=data.channel_id,
        title=data.title,
        description=data.description,
        assigned_to=data.assigned_to,
        priority=data.priority,
        created_by=data.created_by
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_channel_tasks(
    db: Session,
    channel_id: int
):
    stmt = (
        select(ChannelTask)
        .where(
            ChannelTask.channel_id
            == channel_id
        )
    )

    return paginate(
        db,
        stmt
    )


def get_channel_task(
    db: Session,
    task_id: int
):
    stmt = (
        select(ChannelTask)
        .where(
            ChannelTask.id == task_id
        )
    )

    return db.execute(
        stmt
    ).scalar_one_or_none()
