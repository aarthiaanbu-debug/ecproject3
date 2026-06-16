from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str | None] = mapped_column(String, default="pending")  # pending/approved/rejected
    sla_status: Mapped[str | None] = mapped_column(String, nullable=True)
    sla_due_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_escalated: Mapped[bool | None] = mapped_column(Boolean, default=False)
    current_escalation_to: Mapped[int | None] = mapped_column(Integer, nullable=True)
