from pydantic import BaseModel


class ChannelCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    name: str
    description: str | None = None
    channel_type: str
    created_by: int


class ChannelUpdate(BaseModel):
    name: str
    description: str | None = None
    channel_type: str