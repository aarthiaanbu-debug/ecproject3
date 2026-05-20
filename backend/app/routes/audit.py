from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.audit_service import (
    get_audit_logs
)

router = APIRouter(tags=["Audit Logs"])


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/audit-logs")
def audit_logs(
    db: Session = Depends(get_db)
):

    return get_audit_logs(db)