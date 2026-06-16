from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Organization(Base):

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str | None] = mapped_column(String)
    domain: Mapped[str | None] = mapped_column(String, nullable=True)
    plan: Mapped[str | None] = mapped_column(String, default="basic")
    is_active: Mapped[int | None] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)


class TenantUsage(Base):

    __tablename__ = "tenant_usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int | None] = mapped_column(Integer, index=True)
    users_count: Mapped[int | None] = mapped_column(Integer, default=0)
    tasks_count: Mapped[int | None] = mapped_column(Integer, default=0)
    approvals_count: Mapped[int | None] = mapped_column(Integer, default=0)
    documents_count: Mapped[int | None] = mapped_column(Integer, default=0)
    comments_count: Mapped[int | None] = mapped_column(Integer, default=0)
    notifications_count: Mapped[int | None] = mapped_column(Integer, default=0)
    last_activity_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
