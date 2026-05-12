from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.task_service import (
    create_task_service,
    get_tasks_service,
    update_task_service,
    delete_task_service,
    assign_task_service
)
from app.utils.deps import get_current_user

router = APIRouter(tags=["Task"])


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
    return create_task_service(
        db,
        title,
        description
    )


# =========================
# GET ALL TASKS
# =========================

@router.get("/task/all")
def get_tasks(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_tasks_service(db)


# =========================
# UPDATE TASK
# =========================

@router.put("/task/update/{task_id}")
def update_task(
    task_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    return update_task_service(
        db,
        task_id,
        status
    )


# =========================
# DELETE TASK
# =========================

@router.delete("/task/delete/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    return delete_task_service(
        db,
        task_id
    )


# =========================
# ASSIGN TASK
# =========================

@router.put("/task/assign/{task_id}")
def assign_task(
    task_id: int,
    user: str,
    db: Session = Depends(get_db)
):
    return assign_task_service(
        db,
        task_id,
        user
    )