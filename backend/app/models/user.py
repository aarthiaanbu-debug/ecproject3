from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String)

    email: Mapped[str] = mapped_column(String, unique=True)

    password: Mapped[str] = mapped_column(String)

    role: Mapped[str] = mapped_column(
        String,
        default="employee"
    )

    organization_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )