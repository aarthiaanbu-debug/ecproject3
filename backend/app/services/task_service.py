from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.notification import Notification
from app.models.audit import AuditLog

# =========================
# CREATE TASK SERVICE
# =========================

def create_task_service(
    db: Session,
    title: str,
    description: str
):

    task = Task(
        title=title,
        description=description,
        status="todo",
        assigned_to="Aarthi"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    # NOTIFICATION
    notification = Notification(
        user_id=1,
        message=f"New task created: {task.title}",
        is_read=False
    )

    db.add(notification)

    # AUDIT LOG
    audit = AuditLog(
        user_id=1,
        action="TASK_CREATED",
        entity="Task",
        entity_id=task.id
    )

    db.add(audit)

    db.commit()

    return {
        "message": "Task created successfully",
        "task": task
    }
from app.models.task import Task

def get_tasks_service(
    db,
    current_user
):

    tasks = db.query(Task).filter(
        Task.organization_id == current_user.organization_id
    ).all()

    return tasks


# =========================
# GET TASKS SERVICE
# =========================

def get_tasks_service(
    db: Session,
    page: int,
    limit: int
):

    skip = (page - 1) * limit

    tasks = db.query(Task).offset(skip).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "data": tasks
    }


# =========================
# UPDATE TASK SERVICE
# =========================

from app.models.task import Task

from app.services.audit_service import (
    create_audit_log
)

from app.services.kanban_service import (
    broadcast_kanban_update
)

async def update_task_service(
    db,
    task_id,
    status
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return {
            "message": "Task not found"
        }

    # UPDATE STATUS
    task.status = status

    db.commit()

    # AUDIT LOG
    create_audit_log(
        db,
        "Task Updated",
        "Aarthi"
    )

    # LIVE KANBAN UPDATE
    await broadcast_kanban_update(
        f"Task {task.title} moved to {status}"
    )

    return {
        "message": "Task updated successfully"
    }

# =========================
# DELETE TASK SERVICE
# =========================

def delete_task_service(
    db: Session,
    task_id: int
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return {
            "message": "Task not found"
        }

    # NOTIFICATION
    notification = Notification(
        user_id=1,
        message=f"Task deleted: {task.title}",
        is_read=False
    )

    db.add(notification)

    # AUDIT LOG
    audit = AuditLog(
        user_id=1,
        action="TASK_DELETED",
        entity="Task",
        entity_id=task.id
    )

    db.add(audit)

    db.delete(task)

    db.commit()

    return {
        "message": "Task deleted successfully"
    }


# =========================
# ASSIGN TASK SERVICE
# =========================

def assign_task_service(
    db: Session,
    task_id: int,
    user: str
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return {
            "message": "Task not found"
        }

    task.assigned_to = user

    # NOTIFICATION
    notification = Notification(
        user_id=1,
        message=f"Task assigned to {user}",
        is_read=False
    )

    db.add(notification)

    # AUDIT LOG
    audit = AuditLog(
        user_id=1,
        action="TASK_ASSIGNED",
        entity="Task",
        entity_id=task.id
    )

    db.add(audit)

    db.commit()

    return {
        "message": f"Task assigned to {user}"
    }