from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.notification import Notification

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# =========================
# DATABASE
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# GET ALL NOTIFICATIONS
# =========================

@router.get("/")
def get_notifications(
    db: Session = Depends(get_db)
):

    notifications = db.query(Notification).order_by(
        Notification.id.desc()
    ).all()

    return notifications


# =========================
# CREATE NOTIFICATION
# =========================

@router.post("/create")
def create_notification(
    message: str,
    db: Session = Depends(get_db)
):

    notification = Notification(
        user_id=1,
        message=message,
        is_read=False
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification created successfully",
        "data": notification
    }


# =========================
# MARK AS READ
# =========================

@router.patch("/{id}/read")
def mark_read(
    id: int,
    db: Session = Depends(get_db)
):

    notification = db.query(Notification).filter(
        Notification.id == id
    ).first()

    if not notification:
        return {
            "message": "Notification not found"
        }

    notification.is_read = True

    db.commit()

    return {
        "message": "Notification marked as read"
    }


# =========================
# DELETE NOTIFICATION
# =========================

@router.delete("/delete/{id}")
def delete_notification(
    id: int,
    db: Session = Depends(get_db)
):

    notification = db.query(Notification).filter(
        Notification.id == id
    ).first()

    if not notification:
        return {
            "message": "Notification not found"
        }

    db.delete(notification)
    db.commit()

    return {
        "message": "Notification deleted successfully"
    }