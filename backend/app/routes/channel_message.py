from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.database import get_db

from app.schemas.channel_message_schema import (
    ChannelMessageCreate,
    ChannelMessageUpdate,
    ChannelMessageResponse
)

from app.services.channel_message_service import (
    create_channel_message,
    get_channel_messages,
    update_channel_message,
    delete_channel_message
)

router = APIRouter(
    prefix="/channel-messages",
    tags=["Channel Messages"]
)


@router.post(
    "",
    response_model=ChannelMessageResponse
)
def create(
    data: ChannelMessageCreate,
    db: Session = Depends(get_db)
):
    return create_channel_message(
        db,
        data
    )


@router.get(
    "/{channel_id}",
    response_model=Page[
        ChannelMessageResponse
    ]
)
def list_messages(
    channel_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_channel_messages(
        db,
        channel_id,
        tenant_id,
        user_id
    )


@router.put(
    "/{message_id}",
    response_model=ChannelMessageResponse
)
def update(
    message_id: int,
    data: ChannelMessageUpdate,
    db: Session = Depends(get_db)
):
    return update_channel_message(
        db,
        message_id,
        data
    )


@router.delete(
    "/{message_id}"
)
def delete(
    message_id: int,
    db: Session = Depends(get_db)
):
    return delete_channel_message(
        db,
        message_id
    )
