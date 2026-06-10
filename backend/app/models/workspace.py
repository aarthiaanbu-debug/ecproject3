from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from app.database import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(Integer, nullable=False)

    name = Column(String, nullable=False)

    slug = Column(String, unique=True, nullable=False)

    description = Column(Text, nullable=True)

    avatar_url = Column(String, nullable=True)

    visibility = Column(String, default="PRIVATE")

    created_by = Column(Integer, nullable=False)

    is_archived = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )