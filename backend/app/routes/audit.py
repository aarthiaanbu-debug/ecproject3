from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.audit_service import get_audit_logs_service

router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_logs(
    db: Session = Depends(get_db)
):
    return get_audit_logs_service(db)