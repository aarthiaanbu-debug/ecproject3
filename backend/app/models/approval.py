from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.database import Base

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    status = Column(String, default="pending")  # pending/approved/rejected
    sla_status = Column(String, nullable=True)
    sla_due_time = Column(DateTime, nullable=True)
    is_escalated = Column(Boolean, default=False)
    current_escalation_to = Column(Integer, nullable=True)
