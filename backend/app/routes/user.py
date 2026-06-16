from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User

router = APIRouter(tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.execute(select(User)).scalars().all()
