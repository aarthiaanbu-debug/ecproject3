from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    role_name: Mapped[str] = mapped_column(
        String(100)
    )

    module_name: Mapped[str] = mapped_column(
        String(100)
    )

    can_create: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    can_read: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    can_update: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    can_delete: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )