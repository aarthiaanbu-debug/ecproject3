from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.task import Task


def get_kanban_board_service(db: Session):
    todo_stmt = select(Task).where(Task.status == "todo")
    inprogress_stmt = select(Task).where(Task.status == "inprogress")
    done_stmt = select(Task).where(Task.status == "done")

    return {
        "todo": db.execute(todo_stmt).scalars().all(),
        "inprogress": db.execute(inprogress_stmt).scalars().all(),
        "done": db.execute(done_stmt).scalars().all(),
    }
from app.routes.websocket import active_connections

async def broadcast_kanban_update(message: str):

    for connection in active_connections:
        await connection.send_text(message)
