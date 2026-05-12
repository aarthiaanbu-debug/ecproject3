from sqlalchemy.orm import Session
from app.models.task import Task


def get_kanban_board_service(db: Session):
    return {
        "todo": db.query(Task).filter(Task.status == "todo").all(),
        "in_progress": db.query(Task).filter(Task.status == "in_progress").all(),
        "done": db.query(Task).filter(Task.status == "done").all(),
    }