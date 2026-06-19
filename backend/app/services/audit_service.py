from sqlalchemy import select

from app.models.audit import AuditLog


def create_audit_log(
    db,
    action,
    user="System",
    details=None,
    user_id=1,
    module_name=None,
    action_type=None,
    record_id=None,
    old_data=None,
    new_data=None,
    ip_address=None,
    user_agent=None,
):

    log = AuditLog(
        action=action,
        user=user,
        details=details,
        user_id=user_id,
        module_name=module_name,
        action_type=action_type,
        record_id=record_id,
        old_data=old_data,
        new_data=new_data,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    db.add(log)

    db.commit()

    db.refresh(log)

    return log


def get_audit_logs(db):

    stmt = select(AuditLog)

    logs = db.execute(stmt).scalars().all()

    return logs


def get_audit_log(db, log_id):
    stmt = select(AuditLog).where(AuditLog.id == log_id)

    return db.execute(stmt).scalar_one_or_none()


def get_audit_logs_by_module(db, module_name):
    stmt = (
        select(AuditLog)
        .where(AuditLog.module_name.ilike(module_name))
    )

    return db.execute(stmt).scalars().all()


def get_audit_logs_by_user(db, user_id):
    stmt = select(AuditLog).where(AuditLog.user_id == user_id)

    return db.execute(stmt).scalars().all()


def get_audit_logs_by_date_range(db, start_date, end_date):
    stmt = select(AuditLog)

    if start_date:
        stmt = stmt.where(AuditLog.created_at >= start_date)

    if end_date:
        stmt = stmt.where(AuditLog.created_at <= end_date)

    return db.execute(stmt).scalars().all()
