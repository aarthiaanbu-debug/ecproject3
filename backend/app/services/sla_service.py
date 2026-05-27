from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.models.approval import Approval
from app.models.sla import SLARule, SLATracking
from app.models.task import Task


def create_sla_rule(db, payload):
    rule = SLARule(**payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def list_sla_rules(db):
    return db.query(SLARule).all()


def get_sla_rule(db, rule_id):
    rule = db.query(SLARule).filter(SLARule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="SLA rule not found")
    return rule


def update_sla_rule(db, rule_id, payload):
    rule = get_sla_rule(db, rule_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule


def disable_sla_rule(db, rule_id):
    rule = get_sla_rule(db, rule_id)
    rule.is_active = False
    db.commit()
    db.refresh(rule)
    return rule


def find_rule(db, module_name, priority="medium"):
    return (
        db.query(SLARule)
        .filter(
            SLARule.module_name == module_name,
            SLARule.priority == priority,
            SLARule.is_active == True,
        )
        .first()
        or db.query(SLARule)
        .filter(SLARule.module_name == module_name, SLARule.is_active == True)
        .first()
    )


def start_tracking(db, module_name, record_id):
    existing = (
        db.query(SLATracking)
        .filter(
            SLATracking.module_name == module_name,
            SLATracking.record_id == record_id,
            SLATracking.status == "active",
        )
        .first()
    )
    if existing:
        return existing

    record = get_tracked_record(db, module_name, record_id)
    priority = getattr(record, "priority", None) or "medium"
    rule = find_rule(db, module_name, priority)
    allowed_hours = rule.allowed_hours if rule else 24
    now = datetime.utcnow()
    due_time = now + timedelta(hours=allowed_hours)

    tracking = SLATracking(
        module_name=module_name,
        record_id=record_id,
        sla_rule_id=rule.id if rule else None,
        start_time=now,
        due_time=due_time,
        status="active",
    )
    db.add(tracking)

    record.sla_status = "active"
    record.sla_due_time = due_time
    if hasattr(record, "is_sla_breached"):
        record.is_sla_breached = False

    db.commit()
    db.refresh(tracking)
    return tracking


def complete_tracking(db, tracking_id):
    tracking = db.query(SLATracking).filter(SLATracking.id == tracking_id).first()
    if not tracking:
        raise HTTPException(status_code=404, detail="SLA tracking record not found")
    if tracking.completed_time:
        raise HTTPException(status_code=400, detail="SLA already completed")

    now = datetime.utcnow()
    tracking.completed_time = now
    tracking.status = "completed_within_sla" if now <= tracking.due_time else "breached"
    if tracking.status == "breached":
        tracking.breach_reason = "Completed after SLA due time"

    record = get_tracked_record(db, tracking.module_name, tracking.record_id)
    record.sla_status = tracking.status
    if hasattr(record, "is_sla_breached"):
        record.is_sla_breached = tracking.status == "breached"

    db.commit()
    db.refresh(tracking)
    return tracking


def list_active_tracking(db):
    refresh_breaches(db)
    return db.query(SLATracking).filter(SLATracking.status == "active").all()


def list_breached_tracking(db):
    refresh_breaches(db)
    return db.query(SLATracking).filter(SLATracking.status == "breached").all()


def list_module_tracking(db, module_name):
    refresh_breaches(db)
    return db.query(SLATracking).filter(SLATracking.module_name == module_name).all()


def get_record_tracking(db, module_name, record_id):
    refresh_breaches(db)
    return (
        db.query(SLATracking)
        .filter(SLATracking.module_name == module_name, SLATracking.record_id == record_id)
        .all()
    )


def refresh_breaches(db):
    now = datetime.utcnow()
    active = db.query(SLATracking).filter(SLATracking.status == "active").all()
    changed = False
    for tracking in active:
        if tracking.due_time < now:
            tracking.status = "breached"
            tracking.breach_reason = "SLA due time passed"
            record = get_tracked_record(db, tracking.module_name, tracking.record_id)
            record.sla_status = "breached"
            if hasattr(record, "is_sla_breached"):
                record.is_sla_breached = True
            changed = True
    if changed:
        db.commit()


def get_tracked_record(db, module_name, record_id):
    normalized = module_name.lower()
    model = Task if normalized in {"task", "tasks"} else Approval
    record = db.query(model).filter(model.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{module_name} record not found",
        )
    return record
