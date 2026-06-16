# backend/app/models/notification.py

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    message: Mapped[str] = mapped_column(String, nullable=False)

    is_read: Mapped[bool | None] = mapped_column(Boolean, default=False)
    notification_type: Mapped[str | None] = mapped_column(String, default="general")
    priority: Mapped[str | None] = mapped_column(String, default="normal")

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
