from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime

from app.database import Base

class Document(Base):

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    file_name: Mapped[str | None] = mapped_column(String)

    file_path: Mapped[str | None] = mapped_column(String)

    version: Mapped[str | None] = mapped_column(String)

    task_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("tasks.id")
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
