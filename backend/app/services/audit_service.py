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

    logs = db.query(AuditLog).all()

    return logs


def get_audit_log(db, log_id):
    return db.query(AuditLog).filter(AuditLog.id == log_id).first()


def get_audit_logs_by_module(db, module_name):
    return (
        db.query(AuditLog)
        .filter(AuditLog.module_name.ilike(module_name))
        .all()
    )


def get_audit_logs_by_user(db, user_id):
    return db.query(AuditLog).filter(AuditLog.user_id == user_id).all()


def get_audit_logs_by_date_range(db, start_date, end_date):
    query = db.query(AuditLog)

    if start_date:
        query = query.filter(AuditLog.created_at >= start_date)

    if end_date:
        query = query.filter(AuditLog.created_at <= end_date)

    return query.all()
