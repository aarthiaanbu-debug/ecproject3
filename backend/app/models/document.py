from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime

from app.database import Base

class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    file_name = Column(String)

    file_path = Column(String)

    version = Column(String)

    task_id = Column(
        Integer,
        ForeignKey("tasks.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )