from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    workspace_id: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    role: Mapped[str | None] = mapped_column(String, default="Member")

    joined_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    is_active: Mapped[bool | None] = mapped_column(Boolean, default=True)
