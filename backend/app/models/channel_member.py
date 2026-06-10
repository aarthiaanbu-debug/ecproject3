from sqlalchemy import Column, Integer, Boolean, DateTime
from datetime import datetime
from app.database import Base


class ChannelMember(Base):
    __tablename__ = "channel_members"

    id = Column(Integer, primary_key=True, index=True)

    channel_id = Column(Integer, nullable=False)

    user_id = Column(Integer, nullable=False)

    joined_at = Column(DateTime, default=datetime.utcnow)

    is_muted = Column(Boolean, default=False)

    last_read_message_id = Column(Integer, nullable=True)