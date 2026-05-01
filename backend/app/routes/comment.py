from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.comment import Comment

router = APIRouter(tags=["Comments"])
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/comment/create")
def create_comment(task_id: int, message: str, user: str, db: Session = Depends(get_db)):
    c = Comment(task_id=task_id, message=message, user=user)
    db.add(c)
    db.commit()
    return {"message": "Comment added"}

@router.get("/comment/{task_id}")
def get_comments(task_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.task_id == task_id).all()