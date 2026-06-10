from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app.database import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=True)

    user = Column(String, nullable=True)

    action = Column(String, nullable=True)

    details = Column(Text, nullable=True)

    module_name = Column(String, nullable=True)

    action_type = Column(String, nullable=True)

    record_id = Column(Integer, nullable=True)

    old_data = Column(Text, nullable=True)

    new_data = Column(Text, nullable=True)

    ip_address = Column(String, nullable=True)

    user_agent = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
