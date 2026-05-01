from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.task import Task

router = APIRouter(tags=["Kanban"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET KANBAN BOARD
@router.get("/kanban")
def get_kanban(db: Session = Depends(get_db)):
    todo = db.query(Task).filter(Task.status == "todo").all()
    progress = db.query(Task).filter(Task.status == "inprogress").all()
    done = db.query(Task).filter(Task.status == "done").all()

    return {
        "todo": todo,
        "inprogress": progress,
        "done": done
    }