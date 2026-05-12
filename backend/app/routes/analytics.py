from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.task import Task

router = APIRouter(tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    total = db.query(Task).count()
    todo = db.query(Task).filter(Task.status == "todo").count()
    progress = db.query(Task).filter(Task.status == "inprogress").count()
    done = db.query(Task).filter(Task.status == "done").count()

    return {
        "total": total,
        "todo": todo,
        "inprogress": progress,
        "done": done
    }