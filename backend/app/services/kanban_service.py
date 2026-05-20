from sqlalchemy.orm import Session
from app.models.task import Task


def get_kanban_board_service(db: Session):
    return {
        "todo": db.query(Task).filter(Task.status == "todo").all(),
        "in_progress": db.query(Task).filter(Task.status == "in_progress").all(),
        "done": db.query(Task).filter(Task.status == "done").all(),
    }
from app.routes.websocket import active_connections

async def broadcast_kanban_update(message: str):

    for connection in active_connections:
        await connection.send_text(message)