from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class ChannelMessage(Base):
    __tablename__ = "channel_messages"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    tenant_id: Mapped[int] = mapped_column()

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id")
    )

    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channels.id")
    )

    sender_id: Mapped[int] = mapped_column()

    content: Mapped[str] = mapped_column(
        Text
    )

    message_type: Mapped[str] = mapped_column(
        String(50),
        default="TEXT"
    )

    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )