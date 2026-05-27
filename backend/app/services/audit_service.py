from app.models.audit import AuditLog


def create_audit_log(
    db,
    action,
    user,
    details
):

    log = AuditLog(
        action=action,
        user=user,
        details=details
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
    return db.query(AuditLog).filter(AuditLog.module_name == module_name).all()


def get_audit_logs_by_user(db, user_id):
    return db.query(AuditLog).filter(AuditLog.user_id == user_id).all()


def get_audit_logs_by_date_range(db, start_date, end_date):
    query = db.query(AuditLog)

    if start_date:
        query = query.filter(AuditLog.created_at >= start_date)

    if end_date:
        query = query.filter(AuditLog.created_at <= end_date)

    return query.all()
