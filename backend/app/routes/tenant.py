from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.tenant_schema import TenantCreate, TenantUpdate, TenantUserAssign
from app.services import tenant_service

router = APIRouter(prefix="/tenants", tags=["Tenant Collaboration Usage"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db)):
    return tenant_service.create_tenant(db, payload)


@router.get("")
def list_tenants(db: Session = Depends(get_db)):
    return tenant_service.list_tenants(db)


@router.get("/usage")
def list_usage(db: Session = Depends(get_db)):
    return tenant_service.list_tenant_usage(db)


@router.post("/assign-user")
def assign_user(payload: TenantUserAssign, db: Session = Depends(get_db)):
    return tenant_service.assign_user_to_tenant(db, payload)


@router.get("/{tenant_id}")
def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    return tenant_service.get_tenant(db, tenant_id)


@router.put("/{tenant_id}")
def update_tenant(
    tenant_id: int, payload: TenantUpdate, db: Session = Depends(get_db)
):
    return tenant_service.update_tenant(db, tenant_id, payload)


@router.get("/{tenant_id}/users")
def tenant_users(tenant_id: int, db: Session = Depends(get_db)):
    return tenant_service.tenant_users(db, tenant_id)


@router.get("/{tenant_id}/usage")
def tenant_usage(tenant_id: int, db: Session = Depends(get_db)):
    return tenant_service.get_tenant_usage(db, tenant_id)
