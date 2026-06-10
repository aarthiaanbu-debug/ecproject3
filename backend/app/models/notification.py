# backend/app/models/notification.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)

    message = Column(String, nullable=False)

    is_read = Column(Boolean, default=False)
    notification_type = Column(String, default="general")
    priority = Column(String, default="normal")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
