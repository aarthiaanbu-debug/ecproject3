from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.leave_schema import LeaveRequestCreate
from app.services import leave_service

router = APIRouter(prefix="/leave-requests", tags=["Leave Requests"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def create_leave_request(payload: LeaveRequestCreate, db: Session = Depends(get_db)):
    return leave_service.create_leave_request(db, payload)


@router.get("")
def list_leave_requests(db: Session = Depends(get_db)):
    return leave_service.list_leave_requests(db)


@router.put("/{leave_id}/status")
def update_leave_status(
    leave_id: int,
    status: str,
    approved_by: int = 1,
    db: Session = Depends(get_db),
):
    return leave_service.update_leave_status(db, leave_id, status, approved_by)
