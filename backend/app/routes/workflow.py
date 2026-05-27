from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.phase9_schema import (
    DelegationCreate,
    EscalationCreate,
    NotificationPreferenceUpdate,
)
from app.services import workflow_service

router = APIRouter(tags=["Workflow Governance"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/approval-escalations")
def create_escalation(payload: EscalationCreate, db: Session = Depends(get_db)):
    return workflow_service.create_escalation(db, payload)


@router.get("/approval-escalations")
def list_escalations(db: Session = Depends(get_db)):
    return workflow_service.list_escalations(db)


@router.get("/approval-escalations/pending")
def pending_escalations(db: Session = Depends(get_db)):
    return workflow_service.list_pending_escalations(db)


@router.get("/approval-escalations/approval/{approval_id}")
def approval_escalation_history(approval_id: int, db: Session = Depends(get_db)):
    return workflow_service.escalation_history(db, approval_id)


@router.put("/approval-escalations/{escalation_id}/resolve")
def resolve_escalation(escalation_id: int, db: Session = Depends(get_db)):
    return workflow_service.set_escalation_status(db, escalation_id, "resolved")


@router.put("/approval-escalations/{escalation_id}/cancel")
def cancel_escalation(escalation_id: int, db: Session = Depends(get_db)):
    return workflow_service.set_escalation_status(db, escalation_id, "cancelled")


@router.post("/approval-delegations")
def create_delegation(payload: DelegationCreate, db: Session = Depends(get_db)):
    return workflow_service.create_delegation(db, payload)


@router.get("/approval-delegations/me")
def my_delegations(db: Session = Depends(get_db)):
    return workflow_service.my_delegations(db)


@router.get("/approval-delegations/active")
def active_delegations(db: Session = Depends(get_db)):
    return workflow_service.active_delegations(db)


@router.put("/approval-delegations/{delegation_id}/cancel")
def cancel_delegation(delegation_id: int, db: Session = Depends(get_db)):
    return workflow_service.cancel_delegation(db, delegation_id)


@router.get("/notification-preferences/me")
def my_notification_preferences(db: Session = Depends(get_db)):
    return workflow_service.get_or_create_preferences(db)


@router.put("/notification-preferences/me")
def update_my_notification_preferences(
    payload: NotificationPreferenceUpdate, db: Session = Depends(get_db)
):
    return workflow_service.update_preferences(db, payload)


@router.post("/notification-preferences/default/{user_id}")
def create_default_preferences(user_id: int, db: Session = Depends(get_db)):
    return workflow_service.get_or_create_preferences(db, user_id)
