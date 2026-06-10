from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.analytics_service import get_analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])
dashboard_router = APIRouter(tags=["Role Dashboards"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def analytics(db: Session = Depends(get_db)):
    return get_analytics_service(db)

# =========================
# EMPLOYEE DASHBOARD
# =========================

@router.get("/employee")
def employee_dashboard():

    return {
        "tasks": 10,
        "pending_requests": 3
    }


# =========================
# MANAGER DASHBOARD
# =========================

@router.get("/manager")
def manager_dashboard():

    return {
        "team_tasks": 50,
        "approvals_pending": 7
    }


# =========================
# ADMIN DASHBOARD
# =========================

@router.get("/admin")
def admin_dashboard():

    return {
        "users": 100,
        "documents": 250,
        "active_tasks": 80
    }


@dashboard_router.get("/employee/dashboard")
def employee_dashboard_alias():
    return employee_dashboard()


@dashboard_router.get("/manager/dashboard")
def manager_dashboard_alias():
    return manager_dashboard()


@dashboard_router.get("/admin/dashboard")
def admin_dashboard_alias():
    return admin_dashboard()
