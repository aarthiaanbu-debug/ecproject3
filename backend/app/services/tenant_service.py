from datetime import datetime

from fastapi import HTTPException

from app.models.approval import Approval
from app.models.comment import Comment
from app.models.document import Document
from app.models.notification import Notification
from app.models.organization import Organization, TenantUsage
from app.models.task import Task
from app.models.user import User


def create_tenant(db, payload):
    tenant = Organization(**payload.model_dump())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    refresh_tenant_usage(db, tenant.id)
    return tenant


def list_tenants(db):
    return db.query(Organization).all()


def get_tenant(db, tenant_id):
    tenant = db.query(Organization).filter(Organization.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


def update_tenant(db, tenant_id, payload):
    tenant = get_tenant(db, tenant_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(tenant, key, value)
    db.commit()
    db.refresh(tenant)
    return tenant


def assign_user_to_tenant(db, payload):
    tenant = get_tenant(db, payload.organization_id)
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.organization_id = tenant.id
    db.commit()
    db.refresh(user)
    refresh_tenant_usage(db, tenant.id)
    return user


def tenant_users(db, tenant_id):
    get_tenant(db, tenant_id)
    return db.query(User).filter(User.organization_id == tenant_id).all()


def refresh_tenant_usage(db, tenant_id):
    get_tenant(db, tenant_id)
    usage = (
        db.query(TenantUsage)
        .filter(TenantUsage.organization_id == tenant_id)
        .first()
    )
    if not usage:
        usage = TenantUsage(organization_id=tenant_id)
        db.add(usage)

    usage.users_count = db.query(User).filter(User.organization_id == tenant_id).count()
    usage.tasks_count = db.query(Task).filter(Task.organization_id == tenant_id).count()
    usage.approvals_count = db.query(Approval).count()
    usage.documents_count = db.query(Document).count()
    usage.comments_count = db.query(Comment).count()
    usage.notifications_count = db.query(Notification).count()
    usage.last_activity_at = datetime.utcnow()
    db.commit()
    db.refresh(usage)
    return usage


def get_tenant_usage(db, tenant_id):
    return refresh_tenant_usage(db, tenant_id)


def list_tenant_usage(db):
    tenant_ids = [tenant.id for tenant in db.query(Organization).all()]
    return [refresh_tenant_usage(db, tenant_id) for tenant_id in tenant_ids]
