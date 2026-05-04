from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models.task import Task
from app.models.notification import Notification
from app.models.audit_log import AuditLog
from app.utils.deps import get_current_user

router = APIRouter(tags=["Task"])

Base.metadata.create_all(bind=engine)


# =========================
# DATABASE
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE TASK
# =========================

@router.post("/task/create")
def create_task(
    title: str,
    description: str,
    db: Session = Depends(get_db)
):

    # CREATE TASK
    task = Task(
        title=title,
        description=description,
        status="todo",
        assigned_to="Aarthi"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    # =========================
    # NOTIFICATION
    # =========================

    notification = Notification(
        user_id=1,
        message=f"New task created: {task.title}",
        is_read=False
    )

    db.add(notification)

    # =========================
    # AUDIT LOG
    # =========================

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


# =========================
# GET ALL TASKS
# =========================

@router.get("/task/all")
def get_tasks(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return db.query(Task).all()


# =========================
# UPDATE TASK STATUS
# =========================

@router.put("/task/update/{task_id}")
def update_task(
    task_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return {
            "message": "Task not found"
        }

    task.status = status

    # NOTIFICATION
    notification = Notification(
        user_id=1,
        message=f"Task #{task.id} updated to {status}",
        is_read=False
    )

    db.add(notification)

    # AUDIT LOG
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


# =========================
# DELETE TASK
# =========================

@router.delete("/task/delete/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
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
# ASSIGN TASK
# =========================

@router.put("/task/assign/{task_id}")
def assign_task(
    task_id: int,
    user: str,
    db: Session = Depends(get_db)
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