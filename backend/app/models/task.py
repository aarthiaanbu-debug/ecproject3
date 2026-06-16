from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    status: Mapped[str | None] = mapped_column(String, default="todo")   # todo / inprogress / done
    assigned_to: Mapped[str | None] = mapped_column(String)
    created_by: Mapped[str | None] = mapped_column(String)
    organization_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    priority: Mapped[str | None] = mapped_column(String, default="medium")
    deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    sla_status: Mapped[str | None] = mapped_column(String, nullable=True)
    sla_due_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_sla_breached: Mapped[bool | None] = mapped_column(Boolean, default=False)
