from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.audit_service import (
    get_audit_log,
    get_audit_logs,
    get_audit_logs_by_date_range,
    get_audit_logs_by_module,
    get_audit_logs_by_user,
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


@router.get("/audit-logs/date-range")
def audit_logs_date_range(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    return get_audit_logs_by_date_range(db, start_date, end_date)


@router.get("/audit-logs/{log_id}")
def audit_log_detail(log_id: int, db: Session = Depends(get_db)):
    return get_audit_log(db, log_id)


@router.get("/audit-logs/module/{module_name}")
def audit_logs_module(module_name: str, db: Session = Depends(get_db)):
    return get_audit_logs_by_module(db, module_name)


@router.get("/audit-logs/user/{user_id}")
def audit_logs_user(user_id: int, db: Session = Depends(get_db)):
    return get_audit_logs_by_user(db, user_id)
