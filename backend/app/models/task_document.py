from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class TaskDocument(Base):
    __tablename__ = "task_documents"

    id: Mapped[int] = mapped_column(primary_key=True)

    tenant_id: Mapped[int]

    task_id: Mapped[int] = mapped_column(
        ForeignKey("workspace_tasks.id")
    )

    uploaded_by: Mapped[int]

    file_name: Mapped[str] = mapped_column(
        String(255)
    )

    file_path: Mapped[str] = mapped_column(
        String(500)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )