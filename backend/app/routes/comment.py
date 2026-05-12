from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.comment_service import (
    get_comments_service,
    add_comment_service
)

router = APIRouter(prefix="/comments", tags=["Comments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{task_id}")
def get_comments(task_id: int, db: Session = Depends(get_db)):
    return get_comments_service(db, task_id)


@router.post("/{task_id}")
def add_comment(task_id: int, content: str, db: Session = Depends(get_db)):
    return add_comment_service(db, task_id, content)