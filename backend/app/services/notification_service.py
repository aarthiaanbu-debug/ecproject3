from app.models.notification import Notification


def get_notifications(db):

    return db.query(Notification).all()


def mark_read(
    db,
    notification_id
):

    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:

        return {
            "message": "Notification not found"
        }

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification