from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    from_date = Column(String, nullable=False)
    to_date = Column(String, nullable=False)
    status = Column(String, default="pending")
    requested_by = Column(Integer, nullable=True)
    approved_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
