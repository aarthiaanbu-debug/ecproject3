from datetime import datetime, time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
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
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
):
    parsed_start = parse_date_filter(start_date, is_end_date=False)
    parsed_end = parse_date_filter(end_date, is_end_date=True)

    return get_audit_logs_by_date_range(db, parsed_start, parsed_end)


def parse_date_filter(value: Optional[str], is_end_date: bool):
    if not value:
        return None

    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
    ]

    for date_format in formats:
        try:
            parsed = datetime.strptime(value, date_format)

            if date_format in {"%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"}:
                parsed_time = time.max if is_end_date else time.min
                return datetime.combine(parsed.date(), parsed_time)

            return parsed
        except ValueError:
            continue

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY. Example: 2026-04-30 or 30-04-2026.",
    )


@router.get("/audit-logs/module/{module_name}")
def audit_logs_module(module_name: str, db: Session = Depends(get_db)):
    return get_audit_logs_by_module(db, module_name)


@router.get("/audit-logs/user/{user_id}")
def audit_logs_user(user_id: int, db: Session = Depends(get_db)):
    return get_audit_logs_by_user(db, user_id)


@router.get("/audit-logs/{log_id}")
def audit_log_detail(log_id: int, db: Session = Depends(get_db)):
    return get_audit_log(db, log_id)
