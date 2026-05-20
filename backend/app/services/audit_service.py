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