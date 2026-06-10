from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.channel_schema import (
    ChannelCreate,
    ChannelUpdate
)

from app.services.channel_service import (
    create_channel,
    get_channels,
    get_channel,
    update_channel,
    archive_channel,
    restore_channel,
    join_channel,
    leave_channel
)

router = APIRouter(
    prefix="/channels",
    tags=["Channels"]
)


# CREATE CHANNEL
@router.post("")
def create(
    data: ChannelCreate,
    db: Session = Depends(get_db)
):
    return create_channel(db, data)


# LIST CHANNELS BY WORKSPACE
@router.get("/workspace/{workspace_id}")
def list_channels(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    return get_channels(
        db,
        workspace_id
    )


# GET SINGLE CHANNEL
@router.get("/{channel_id}")
def get_one(
    channel_id: int,
    db: Session = Depends(get_db)
):
    return get_channel(
        db,
        channel_id
    )


# UPDATE CHANNEL
@router.put("/{channel_id}")
def update(
    channel_id: int,
    data: ChannelUpdate,
    db: Session = Depends(get_db)
):
    return update_channel(
        db,
        channel_id,
        data
    )


# ARCHIVE CHANNEL
@router.patch("/{channel_id}/archive")
def archive(
    channel_id: int,
    db: Session = Depends(get_db)
):
    return archive_channel(
        db,
        channel_id
    )


# RESTORE CHANNEL
@router.patch("/{channel_id}/restore")
def restore(
    channel_id: int,
    db: Session = Depends(get_db)
):
    return restore_channel(
        db,
        channel_id
    )


# JOIN CHANNEL
@router.post("/{channel_id}/join/{user_id}")
def join(
    channel_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    return join_channel(
        db,
        channel_id,
        user_id
    )


# LEAVE CHANNEL
@router.post("/{channel_id}/leave/{user_id}")
def leave(
    channel_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    return leave_channel(
        db,
        channel_id,
        user_id
    )