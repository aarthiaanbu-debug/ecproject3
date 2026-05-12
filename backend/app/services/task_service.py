from app.models.task import Task
from app.models.notification import Notification
from app.models.audit_log import AuditLog


def create_task_service(db, title, description):

    task = Task(
        title=title,
        description=description,
        status="todo",
        assigned_to="Aarthi"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    notification = Notification(
        user_id=1,
        message=f"New task created: {task.title}",
        is_read=False
    )

    db.add(notification)

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


def get_tasks_service(db):

    return db.query(Task).all()


def update_task_service(db, task_id, status):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return {
            "message": "Task not found"
        }

    task.status = status

    notification = Notification(
        user_id=1,
        message=f"Task updated to {status}",
        is_read=False
    )

    db.add(notification)

    audit = AuditLog(
        user_id=1,
        action="TASK_UPDATED",
        entity="Task",
        entity_id=task.id
    )

    db.add(audit)

    db.commit()

    return {
        "message": "Task updated successfully"
    }


def delete_task_service(db, task_id):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return {
            "message": "Task not found"
        }

    db.delete(task)

    notification = Notification(
        user_id=1,
        message=f"Task deleted: {task.title}",
        is_read=False
    )

    db.add(notification)

    audit = AuditLog(
        user_id=1,
        action="TASK_DELETED",
        entity="Task",
        entity_id=task.id
    )

    db.add(audit)

    db.commit()

    return {
        "message": "Task deleted successfully"
    }


def assign_task_service(db, task_id, user):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return {
            "message": "Task not found"
        }

    task.assigned_to = user

    notification = Notification(
        user_id=1,
        message=f"Task assigned to {user}",
        is_read=False
    )

    db.add(notification)

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