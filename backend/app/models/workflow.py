from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ApprovalEscalation(Base):
    __tablename__ = "approval_escalations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    approval_id: Mapped[int] = mapped_column(Integer, ForeignKey("approvals.id"), nullable=False)
    escalated_from: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    escalated_to: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    escalation_level: Mapped[int | None] = mapped_column(Integer, default=1)
    status: Mapped[str | None] = mapped_column(String, default="pending")
    escalated_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ApprovalDelegation(Base):
    __tablename__ = "approval_delegations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    delegator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    delegatee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool | None] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    in_app_enabled: Mapped[bool | None] = mapped_column(Boolean, default=True)
    email_enabled: Mapped[bool | None] = mapped_column(Boolean, default=False)
    task_notifications: Mapped[bool | None] = mapped_column(Boolean, default=True)
    approval_notifications: Mapped[bool | None] = mapped_column(Boolean, default=True)
    escalation_notifications: Mapped[bool | None] = mapped_column(Boolean, default=True)
    document_notifications: Mapped[bool | None] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
