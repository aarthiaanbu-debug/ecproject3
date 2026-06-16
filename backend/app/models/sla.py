from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SLARule(Base):
    __tablename__ = "sla_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    module_name: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[str] = mapped_column(String, nullable=False)
    allowed_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    escalation_enabled: Mapped[bool | None] = mapped_column(Boolean, default=False)
    escalation_after_hours: Mapped[int | None] = mapped_column(Integer, default=0)
    is_active: Mapped[bool | None] = mapped_column(Boolean, default=True)
    created_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SLATracking(Base):
    __tablename__ = "sla_tracking"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    module_name: Mapped[str] = mapped_column(String, nullable=False)
    record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sla_rule_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("sla_rules.id"), nullable=True)
    start_time: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    due_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str | None] = mapped_column(String, default="active")
    breach_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
