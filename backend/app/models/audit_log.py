from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    action = Column(String)

    user = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )