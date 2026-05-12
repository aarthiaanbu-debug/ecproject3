from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.approval_service import (
    get_approvals_service,
    create_approval_service
)

router = APIRouter(prefix="/approval", tags=["Approval"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_approvals(db: Session = Depends(get_db)):
    return get_approvals_service(db)


@router.post("/")
def create_approval(data: dict, db: Session = Depends(get_db)):
    return create_approval_service(db, data)