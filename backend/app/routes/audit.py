from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.audit_log import AuditLog

router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)

# DB CONNECTION

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# GET AUDIT LOGS

@router.get("/")
def get_audit_logs(
    db: Session = Depends(get_db)
):

    logs = db.query(AuditLog).all()

    return logs