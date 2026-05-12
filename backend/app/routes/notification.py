from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.services import notification_service

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_notifications(
    db: Session = Depends(get_db)
):

    return notification_service.get_notifications(db)


@router.put("/{notification_id}")
def mark_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):

    return notification_service.mark_read(
        db,
        notification_id
    )