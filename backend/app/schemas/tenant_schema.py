from typing import Optional

from pydantic import BaseModel


class TenantCreate(BaseModel):
    name: str
    domain: Optional[str] = None
    plan: str = "basic"


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    plan: Optional[str] = None
    is_active: Optional[int] = None


class TenantUserAssign(BaseModel):
    user_id: int
    organization_id: int
