from sqlalchemy import Column, Integer, String,datetime,ForeignKey

from app.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    plan = Column(String)          # pro / premium / gold
    status = Column(String)        # active / inactive
    stripe_session_id = Column(String)
    stripe_payment_intent = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)