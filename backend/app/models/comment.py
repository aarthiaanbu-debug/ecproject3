from sqlalchemy import Column, Integer, String
from app.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    message = Column(String)
    user = Column(String)