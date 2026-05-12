from app.models.audit_log import AuditLog


def get_audit_logs_service(db):

    logs = db.query(AuditLog).all()

    return logs