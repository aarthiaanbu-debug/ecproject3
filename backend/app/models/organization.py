from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class Organization(Base):

    __tablename__ = "organizations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)
    domain = Column(String, nullable=True)
    plan = Column(String, default="basic")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)


class TenantUsage(Base):

    __tablename__ = "tenant_usage"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, index=True)
    users_count = Column(Integer, default=0)
    tasks_count = Column(Integer, default=0)
    approvals_count = Column(Integer, default=0)
    documents_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    notifications_count = Column(Integer, default=0)
    last_activity_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
