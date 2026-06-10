from sqlalchemy import Boolean, Column, DateTime, Integer, String
from datetime import datetime
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="todo")   # todo / inprogress / done
    assigned_to = Column(String) 
    created_by = Column(String)
    organization_id = Column(Integer, nullable=True)
    priority = Column(String, default="medium")
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    sla_status = Column(String, nullable=True)
    sla_due_time = Column(DateTime, nullable=True)
    is_sla_breached = Column(Boolean, default=False)
