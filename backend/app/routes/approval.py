from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.approval import Approval

router = APIRouter(tags=["Approval"])
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/approval/create")
def create_approval(task_id: int, db: Session = Depends(get_db)):
    a = Approval(task_id=task_id)
    db.add(a)
    db.commit()
    return {"message": "Approval requested"}

@router.put("/approval/update/{id}")
def update_approval(id: int, status: str, db: Session = Depends(get_db)):
    a = db.query(Approval).filter(Approval.id == id).first()
    a.status = status
    db.commit()
    return {"message": "Updated"}

@router.get("/approval/all")
def get_approvals(db: Session = Depends(get_db)):
    return db.query(Approval).all()