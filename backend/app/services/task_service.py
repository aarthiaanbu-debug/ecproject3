from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.task import Task
from app.models.notification import Notification
from app.services.audit_service import create_audit_log

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
        assigned_to="Aarthi",
        organization_id=1,
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

    create_audit_log(
        db,
        action="TASK_CREATED",
        user="Aarthi",
        details=f"Task created: {task.title}",
        module_name="Task",
        action_type="Created",
        record_id=task.id,
        new_data=f"title={task.title}; status={task.status}; assigned_to={task.assigned_to}",
    )

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

    stmt = select(Task).where(
        Task.organization_id == current_user.organization_id
    )

    tasks = db.execute(stmt).scalars().all()

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

    stmt = (
        select(Task)
        .offset(skip)
        .limit(limit)
    )

    tasks = db.execute(stmt).scalars().all()

    return {
        "page": page,
        "limit": limit,
        "data": tasks
    }


# =========================
# UPDATE TASK SERVICE
# =========================

from app.models.task import Task

from app.services.kanban_service import (
    broadcast_kanban_update
)

async def update_task_service(
    db,
    task_id,
    status
):

    stmt = select(Task).where(
        Task.id == task_id
    )

    task = db.execute(stmt).scalar_one_or_none()

    if not task:
        return {
            "message": "Task not found"
        }

    old_status = task.status

    # UPDATE STATUS
    task.status = status

    db.commit()

    # AUDIT LOG
    create_audit_log(
        db,
        action="TASK_UPDATED",
        user="Aarthi",
        details=f"Task {task.id} status changed from {old_status} to {status}",
        module_name="Task",
        action_type="Updated",
        record_id=task.id,
        old_data=f"status={old_status}",
        new_data=f"status={status}",
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

    stmt = select(Task).where(
        Task.id == task_id
    )

    task = db.execute(stmt).scalar_one_or_none()

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

    create_audit_log(
        db,
        action="TASK_DELETED",
        user="Aarthi",
        details=f"Task deleted: {task.title}",
        module_name="Task",
        action_type="Deleted",
        record_id=task.id,
        old_data=f"title={task.title}; status={task.status}; assigned_to={task.assigned_to}",
    )

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

    stmt = select(Task).where(
        Task.id == task_id
    )

    task = db.execute(stmt).scalar_one_or_none()

    if not task:
        return {
            "message": "Task not found"
        }

    old_assignee = task.assigned_to
    task.assigned_to = user

    # NOTIFICATION
    notification = Notification(
        user_id=1,
        message=f"Task assigned to {user}",
        is_read=False
    )

    db.add(notification)

    create_audit_log(
        db,
        action="TASK_ASSIGNED",
        user="Aarthi",
        details=f"Task {task.id} assigned to {user}",
        module_name="Task",
        action_type="Updated",
        record_id=task.id,
        old_data=f"assigned_to={old_assignee}",
        new_data=f"assigned_to={user}",
    )

    db.commit()

    return {
        "message": f"Task assigned to {user}"
    }
