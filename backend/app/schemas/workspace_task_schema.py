from datetime import datetime

from pydantic import BaseModel


class WorkspaceTaskCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    title: str
    description: str | None = None
    assigned_to: int | None = None
    priority: str
    due_date: datetime | None = None
    created_by: int


class WorkspaceTaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    assigned_to: int | None
    priority: str
    status: str

    model_config = {
        "from_attributes": True
    }