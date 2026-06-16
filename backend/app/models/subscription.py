from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"))

    plan: Mapped[str | None] = mapped_column(String)          # pro / premium / gold
    status: Mapped[str | None] = mapped_column(String)        # active / inactive
    stripe_session_id: Mapped[str | None] = mapped_column(String)
    stripe_payment_intent: Mapped[str | None] = mapped_column(String)

    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
