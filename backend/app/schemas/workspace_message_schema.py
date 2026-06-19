from datetime import datetime

from pydantic import BaseModel


class WorkspaceMessageCreate(BaseModel):

    tenant_id: int
    workspace_id: int
    user_id: int
    message: str


class WorkspaceMessageUpdate(BaseModel):

    tenant_id: int
    user_id: int
    message: str


class WorkspaceMessageResponse(BaseModel):

    id: int
    tenant_id: int
    workspace_id: int
    user_id: int
    message: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
