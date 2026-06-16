from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ChannelMember(Base):
    __tablename__ = "channel_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    channel_id: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    joined_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    is_muted: Mapped[bool | None] = mapped_column(Boolean, default=False)

    last_read_message_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
