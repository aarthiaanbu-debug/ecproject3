from sqlalchemy import select

from app.models.approval import Approval
from app.services.audit_service import create_audit_log


def get_approvals_service(db):
    stmt = select(Approval)

    return db.execute(stmt).scalars().all()


def create_approval_service(db, data):
    approval = Approval(**data)
    db.add(approval)
    db.commit()
    db.refresh(approval)
    create_audit_log(
        db,
        action="APPROVAL_CREATED",
        user="Aarthi",
        details=f"Approval created for task {approval.task_id}",
        module_name="Approval",
        action_type="Created",
        record_id=approval.id,
        new_data=f"task_id={approval.task_id}; status={approval.status}",
    )
    return {
        "id": approval.id,
        "task_id": approval.task_id,
        "status": approval.status,
        "message": "Approval created",
    }


def update_approval_status_service(db, approval_id, status):
    stmt = (
        select(Approval)
        .where(Approval.id == approval_id)
    )

    approval = db.execute(stmt).scalar_one_or_none()

    if not approval:
        return {"message": "Approval not found"}

    old_status = approval.status
    approval.status = status
    db.commit()
    db.refresh(approval)

    create_audit_log(
        db,
        action="APPROVAL_STATUS_UPDATED",
        user="Aarthi",
        details=f"Approval {approval.id} changed from {old_status} to {status}",
        module_name="Approval",
        action_type="Updated",
        record_id=approval.id,
        old_data=f"status={old_status}",
        new_data=f"status={status}",
    )

    return {
        "id": approval.id,
        "task_id": approval.task_id,
        "status": approval.status,
        "message": "Approval status updated",
    }
