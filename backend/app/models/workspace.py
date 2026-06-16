from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    tenant_id: Mapped[int] = mapped_column(Integer, nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)

    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)

    visibility: Mapped[str | None] = mapped_column(String, default="PRIVATE")

    created_by: Mapped[int] = mapped_column(Integer, nullable=False)

    is_archived: Mapped[bool | None] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
