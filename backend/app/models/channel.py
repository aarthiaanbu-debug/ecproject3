from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    tenant_id: Mapped[int] = mapped_column(Integer, nullable=False)

    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"), nullable=False)

    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), nullable=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    channel_type: Mapped[str | None] = mapped_column(String, default="PUBLIC")

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    is_archived: Mapped[bool | None] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
