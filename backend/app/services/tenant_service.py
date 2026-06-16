from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func, select

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
    return db.execute(select(Organization)).scalars().all()


def get_tenant(db, tenant_id):
    tenant = db.execute(
        select(Organization).where(Organization.id == tenant_id)
    ).scalar_one_or_none()
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
    user = db.execute(
        select(User).where(User.id == payload.user_id)
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.organization_id = tenant.id
    db.commit()
    db.refresh(user)
    refresh_tenant_usage(db, tenant.id)
    return user


def tenant_users(db, tenant_id):
    get_tenant(db, tenant_id)
    return db.execute(
        select(User).where(User.organization_id == tenant_id)
    ).scalars().all()


def refresh_tenant_usage(db, tenant_id):
    get_tenant(db, tenant_id)
    usage = db.execute(
        select(TenantUsage).where(TenantUsage.organization_id == tenant_id)
    ).scalar_one_or_none()
    if not usage:
        usage = TenantUsage(organization_id=tenant_id)
        db.add(usage)

    usage.users_count = db.execute(
        select(func.count()).select_from(User).where(User.organization_id == tenant_id)
    ).scalar()
    usage.tasks_count = db.execute(
        select(func.count()).select_from(Task).where(Task.organization_id == tenant_id)
    ).scalar()
    usage.approvals_count = db.execute(
        select(func.count()).select_from(Approval)
    ).scalar()
    usage.documents_count = db.execute(
        select(func.count()).select_from(Document)
    ).scalar()
    usage.comments_count = db.execute(
        select(func.count()).select_from(Comment)
    ).scalar()
    usage.notifications_count = db.execute(
        select(func.count()).select_from(Notification)
    ).scalar()
    usage.last_activity_at = datetime.utcnow()
    db.commit()
    db.refresh(usage)
    return usage


def get_tenant_usage(db, tenant_id):
    return refresh_tenant_usage(db, tenant_id)


def list_tenant_usage(db):
    tenant_ids = [
        tenant.id
        for tenant in db.execute(select(Organization)).scalars().all()
    ]
    return [refresh_tenant_usage(db, tenant_id) for tenant_id in tenant_ids]
