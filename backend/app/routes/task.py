from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.task import Task
from app.utils.deps import get_current_user

router = APIRouter(tags=["Task"])
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE TASK
@router.post("/task/create")
def create_task(title: str, description: str, db: Session = Depends(get_db)):
    task = Task(title=title, description=description, status="todo")
    db.add(task)
    db.commit()
    return {"message": "Task created"}

@router.get("/task/all")
def get_tasks(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # 👈 இங்க add பண்ணணும்
):
    return db.query(Task).all()

# UPDATE TASK STATUS (KANBAN)
@router.put("/task/update/{task_id}")
def update_task(task_id: int, status: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    task.status = status
    db.commit()
    return {"message": "Updated"}

# DELETE TASK
@router.delete("/task/delete/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    db.commit()
    return {"message": "Deleted"}

# ASSIGN TASK
@router.put("/task/assign/{task_id}")
def assign_task(task_id: int, user: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    task.assigned_to = user
    db.commit()
    return {"message": "Assigned"}