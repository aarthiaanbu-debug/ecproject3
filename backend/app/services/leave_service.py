from sqlalchemy import select

from app.models.leave import LeaveRequest
from app.models.notification import Notification
from app.services.audit_service import create_audit_log


def create_leave_request(db, payload):
    leave = LeaveRequest(**payload.model_dump(), status="pending")
    db.add(leave)
    db.flush()

    db.add(
        Notification(
            user_id=1,
            message=f"Leave request from {leave.employee_name} needs approval",
            is_read=False,
            notification_type="leave",
            priority="high",
        )
    )

    create_audit_log(
        db,
        action="LEAVE_REQUEST_CREATED",
        user=leave.employee_name,
        details=f"Leave requested from {leave.from_date} to {leave.to_date}",
        module_name="Leave",
        action_type="Created",
        record_id=leave.id,
        new_data=f"employee={leave.employee_name}; status={leave.status}",
    )

    db.commit()
    db.refresh(leave)
    return leave


def list_leave_requests(db):
    stmt = (
        select(LeaveRequest)
        .order_by(LeaveRequest.created_at.desc())
    )

    return db.execute(stmt).scalars().all()


def update_leave_status(db, leave_id, status, approved_by=1):
    stmt = select(LeaveRequest).where(LeaveRequest.id == leave_id)

    leave = db.execute(stmt).scalar_one_or_none()

    if not leave:
        return {"message": "Leave request not found"}

    old_status = leave.status
    leave.status = status
    leave.approved_by = approved_by

    db.add(
        Notification(
            user_id=leave.requested_by or 1,
            message=f"Your leave request was {status}",
            is_read=False,
            notification_type="leave",
            priority="normal",
        )
    )

    create_audit_log(
        db,
        action="LEAVE_STATUS_UPDATED",
        user="Manager",
        details=f"Leave request {leave.id} changed from {old_status} to {status}",
        module_name="Leave",
        action_type="Updated",
        record_id=leave.id,
        old_data=f"status={old_status}",
        new_data=f"status={status}",
    )

    db.commit()
    db.refresh(leave)
    return leave
