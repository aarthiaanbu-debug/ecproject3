from datetime import datetime

from fastapi import HTTPException

from app.models.approval import Approval
from app.services.audit_service import create_audit_log
from app.models.workflow import (
    ApprovalDelegation,
    ApprovalEscalation,
    NotificationPreference,
)


def create_escalation(db, payload):
    approval = db.query(Approval).filter(Approval.id == payload.approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")

    escalation = ApprovalEscalation(**payload.model_dump())
    db.add(escalation)
    db.flush()

    approval.is_escalated = True
    approval.current_escalation_to = payload.escalated_to
    if not approval.sla_status:
        approval.sla_status = "escalated"

    db.commit()
    db.refresh(escalation)
    create_audit_log(
        db,
        action="APPROVAL_ESCALATED",
        user="Aarthi",
        details=f"Approval {payload.approval_id} escalated to user {payload.escalated_to}",
        module_name="Approval",
        action_type="Escalated",
        record_id=payload.approval_id,
        new_data=f"escalated_to={payload.escalated_to}; reason={payload.reason}",
    )
    return escalation


def list_escalations(db):
    return db.query(ApprovalEscalation).all()


def list_pending_escalations(db):
    return (
        db.query(ApprovalEscalation)
        .filter(ApprovalEscalation.status == "pending")
        .all()
    )


def escalation_history(db, approval_id):
    return (
        db.query(ApprovalEscalation)
        .filter(ApprovalEscalation.approval_id == approval_id)
        .all()
    )


def set_escalation_status(db, escalation_id, new_status):
    escalation = (
        db.query(ApprovalEscalation)
        .filter(ApprovalEscalation.id == escalation_id)
        .first()
    )
    if not escalation:
        raise HTTPException(status_code=404, detail="Escalation not found")
    if escalation.status != "pending":
        raise HTTPException(status_code=400, detail="Escalation already resolved")

    escalation.status = new_status
    escalation.resolved_at = datetime.utcnow()

    if new_status in {"resolved", "cancelled"}:
        approval = (
            db.query(Approval).filter(Approval.id == escalation.approval_id).first()
        )
        if approval:
            approval.is_escalated = False
            approval.current_escalation_to = None

    db.commit()
    db.refresh(escalation)
    create_audit_log(
        db,
        action=f"ESCALATION_{new_status.upper()}",
        user="Aarthi",
        details=f"Escalation {escalation.id} marked {new_status}",
        module_name="Approval",
        action_type=new_status.title(),
        record_id=escalation.approval_id,
        new_data=f"status={new_status}",
    )
    return escalation


def create_delegation(db, payload):
    conflicts = (
        db.query(ApprovalDelegation)
        .filter(
            ApprovalDelegation.delegator_id == payload.delegator_id,
            ApprovalDelegation.is_active == True,
            ApprovalDelegation.start_date <= payload.end_date,
            ApprovalDelegation.end_date >= payload.start_date,
        )
        .first()
    )
    if conflicts:
        raise HTTPException(status_code=400, detail="Delegation date conflict")

    delegation = ApprovalDelegation(**payload.model_dump())
    db.add(delegation)
    db.commit()
    db.refresh(delegation)
    return delegation


def my_delegations(db, user_id=1):
    return (
        db.query(ApprovalDelegation)
        .filter(ApprovalDelegation.delegator_id == user_id)
        .all()
    )


def active_delegations(db):
    now = datetime.utcnow()
    return (
        db.query(ApprovalDelegation)
        .filter(
            ApprovalDelegation.is_active == True,
            ApprovalDelegation.start_date <= now,
            ApprovalDelegation.end_date >= now,
        )
        .all()
    )


def cancel_delegation(db, delegation_id):
    delegation = (
        db.query(ApprovalDelegation)
        .filter(ApprovalDelegation.id == delegation_id)
        .first()
    )
    if not delegation:
        raise HTTPException(status_code=404, detail="Delegation not found")
    delegation.is_active = False
    db.commit()
    db.refresh(delegation)
    return delegation


def get_or_create_preferences(db, user_id=1):
    prefs = (
        db.query(NotificationPreference)
        .filter(NotificationPreference.user_id == user_id)
        .first()
    )
    if prefs:
        return prefs

    prefs = NotificationPreference(user_id=user_id)
    db.add(prefs)
    db.commit()
    db.refresh(prefs)
    return prefs


def update_preferences(db, payload, user_id=1):
    prefs = get_or_create_preferences(db, user_id)
    for key, value in payload.model_dump().items():
        setattr(prefs, key, value)
    db.commit()
    db.refresh(prefs)
    return prefs
