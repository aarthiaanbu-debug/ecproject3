from sqlalchemy import Column, Integer, String
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="todo")   # todo / inprogress / done
    assigned_to = Column(String)
    created_by = Column(String)