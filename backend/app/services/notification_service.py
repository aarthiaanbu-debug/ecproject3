from sqlalchemy import select

from app.models.notification import Notification


def get_notifications(db):

    stmt = select(Notification)

    return db.execute(stmt).scalars().all()


def mark_read(
    db,
    notification_id
):

    stmt = select(Notification).where(Notification.id == notification_id)

    notification = db.execute(stmt).scalar_one_or_none()

    if not notification:

        return {
            "message": "Notification not found"
        }

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification
