from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class ChannelTask(Base):
    __tablename__ = "channel_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    tenant_id: Mapped[int]

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id")
    )

    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channels.id")
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    assigned_to: Mapped[int | None] = mapped_column(
        nullable=True
    )

    priority: Mapped[str] = mapped_column(
        String(50),
        default="MEDIUM"
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="OPEN"
    )

    created_by: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )