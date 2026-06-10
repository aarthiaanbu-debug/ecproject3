from pydantic import BaseModel


class WorkspaceCreate(BaseModel):
    tenant_id: int
    name: str
    slug: str
    description: str | None = None
    avatar_url: str | None = None
    visibility: str = "PRIVATE"
    created_by: int


class WorkspaceUpdate(BaseModel):
    name: str
    description: str | None = None
    visibility: str