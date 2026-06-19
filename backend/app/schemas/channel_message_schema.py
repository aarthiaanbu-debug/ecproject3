from datetime import datetime

from pydantic import BaseModel


class ChannelMessageCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    channel_id: int
    sender_id: int
    content: str


class ChannelMessageUpdate(BaseModel):
    content: str


class ChannelMessageResponse(BaseModel):
    id: int
    tenant_id: int
    workspace_id: int
    channel_id: int
    sender_id: int
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }