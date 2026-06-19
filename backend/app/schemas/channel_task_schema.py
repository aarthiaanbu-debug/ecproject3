from pydantic import BaseModel


class ChannelTaskCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    channel_id: int
    title: str
    description: str | None = None
    assigned_to: int | None = None
    priority: str
    created_by: int


class ChannelTaskResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str

    model_config = {
        "from_attributes": True
    }