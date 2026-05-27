from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text

from app.database import Base


class SLARule(Base):
    __tablename__ = "sla_rules"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    allowed_hours = Column(Integer, nullable=False)
    escalation_enabled = Column(Boolean, default=False)
    escalation_after_hours = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SLATracking(Base):
    __tablename__ = "sla_tracking"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String, nullable=False)
    record_id = Column(Integer, nullable=False)
    sla_rule_id = Column(Integer, ForeignKey("sla_rules.id"), nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    due_time = Column(DateTime, nullable=False)
    completed_time = Column(DateTime, nullable=True)
    status = Column(String, default="active")
    breach_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
