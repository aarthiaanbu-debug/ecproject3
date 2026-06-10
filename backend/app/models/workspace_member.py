from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base


class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    id = Column(Integer, primary_key=True, index=True)

    workspace_id = Column(Integer, nullable=False)

    user_id = Column(Integer, nullable=False)

    role = Column(String, default="Member")

    joined_at = Column(DateTime, default=datetime.utcnow)

    is_active = Column(Boolean, default=True)