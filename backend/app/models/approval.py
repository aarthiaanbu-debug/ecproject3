from sqlalchemy import Column, Integer, String
from app.database import Base

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    status = Column(String, default="pending")  # pending/approved/rejected