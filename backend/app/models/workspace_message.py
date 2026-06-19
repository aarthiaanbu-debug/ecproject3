from datetime import datetime

from sqlalchemy import (
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class WorkspaceMessage(Base):

    __tablename__ = "workspace_messages"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int] = mapped_column(
        nullable=False
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id")
    )

    user_id: Mapped[int] = mapped_column(
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )