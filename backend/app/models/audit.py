from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    user: Mapped[str | None] = mapped_column(String, nullable=True)

    action: Mapped[str | None] = mapped_column(String, nullable=True)

    details: Mapped[str | None] = mapped_column(Text, nullable=True)

    module_name: Mapped[str | None] = mapped_column(String, nullable=True)

    action_type: Mapped[str | None] = mapped_column(String, nullable=True)

    record_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    old_data: Mapped[str | None] = mapped_column(Text, nullable=True)

    new_data: Mapped[str | None] = mapped_column(Text, nullable=True)

    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)

    user_agent: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
