from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from app.database import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(Integer, nullable=False)

    workspace_id = Column(Integer, nullable=False)

    name = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    channel_type = Column(String, default="PUBLIC")

    created_by = Column(Integer, nullable=False)

    is_archived = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )