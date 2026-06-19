from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.database import get_db

from app.schemas.channel_task_schema import (
    ChannelTaskCreate,
    ChannelTaskResponse
)

from app.services.channel_task_service import (
    create_channel_task,
    get_channel_tasks,
    get_channel_task
)

router = APIRouter(
    prefix="/channel-tasks",
    tags=["Channel Tasks"]
)


@router.post(
    "",
    response_model=ChannelTaskResponse
)
def create(
    data: ChannelTaskCreate,
    db: Session = Depends(get_db)
):
    return create_channel_task(
        db,
        data
    )


@router.get(
    "/channel/{channel_id}",
    response_model=Page[
        ChannelTaskResponse
    ]
)
def list_tasks(
    channel_id: int,
    db: Session = Depends(get_db)
):
    return get_channel_tasks(
        db,
        channel_id
    )


@router.get(
    "/{task_id}",
    response_model=ChannelTaskResponse
)
def get_one(
    task_id: int,
    db: Session = Depends(get_db)
):
    return get_channel_task(
        db,
        task_id
    )