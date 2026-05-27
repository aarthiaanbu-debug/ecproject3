from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.phase9_schema import SLARuleCreate, SLARuleUpdate
from app.services import sla_service

router = APIRouter(tags=["SLA"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sla-rules")
def create_sla_rule(payload: SLARuleCreate, db: Session = Depends(get_db)):
    return sla_service.create_sla_rule(db, payload)


@router.get("/sla-rules")
def list_sla_rules(db: Session = Depends(get_db)):
    return sla_service.list_sla_rules(db)


@router.get("/sla-rules/{rule_id}")
def get_sla_rule(rule_id: int, db: Session = Depends(get_db)):
    return sla_service.get_sla_rule(db, rule_id)


@router.put("/sla-rules/{rule_id}")
def update_sla_rule(
    rule_id: int, payload: SLARuleUpdate, db: Session = Depends(get_db)
):
    return sla_service.update_sla_rule(db, rule_id, payload)


@router.delete("/sla-rules/{rule_id}")
def disable_sla_rule(rule_id: int, db: Session = Depends(get_db)):
    return sla_service.disable_sla_rule(db, rule_id)


@router.post("/sla-tracking/tasks/{task_id}")
def start_task_tracking(task_id: int, db: Session = Depends(get_db)):
    return sla_service.start_tracking(db, "task", task_id)


@router.post("/sla-tracking/approvals/{approval_id}")
def start_approval_tracking(approval_id: int, db: Session = Depends(get_db)):
    return sla_service.start_tracking(db, "approval", approval_id)


@router.put("/sla-tracking/{tracking_id}/complete")
def complete_tracking(tracking_id: int, db: Session = Depends(get_db)):
    return sla_service.complete_tracking(db, tracking_id)


@router.get("/sla-tracking/active")
def active_tracking(db: Session = Depends(get_db)):
    return sla_service.list_active_tracking(db)


@router.get("/sla-tracking/breached")
def breached_tracking(db: Session = Depends(get_db)):
    return sla_service.list_breached_tracking(db)


@router.get("/sla-tracking/module/{module_name}")
def module_tracking(module_name: str, db: Session = Depends(get_db)):
    return sla_service.list_module_tracking(db, module_name)


@router.get("/sla-tracking/record/{module_name}/{record_id}")
def record_tracking(module_name: str, record_id: int, db: Session = Depends(get_db)):
    return sla_service.get_record_tracking(db, module_name, record_id)
