from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


def clean_text(value: str | None) -> str | None:
    if value is None:
        return value
    return value.strip()


class TenantScoped(BaseModel):
    tenant_id: int = Field(gt=0)


class WorkflowCreate(TenantScoped):
    name: str = Field(min_length=2, max_length=180)
    workflow_type: Literal["TASK", "APPROVAL", "PROJECT", "MEETING"]
    description: str | None = None

    _clean_name = field_validator("name")(clean_text)
    _clean_description = field_validator("description")(clean_text)


class WorkflowUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=180)
    workflow_type: Literal["TASK", "APPROVAL", "PROJECT", "MEETING"] | None = None
    description: str | None = None
    is_active: bool | None = None


class WorkflowRead(WorkflowCreate, ORMModel):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class WorkflowRuleCreate(BaseModel):
    trigger_event: str = Field(min_length=2, max_length=100)
    condition_type: str = Field(min_length=2, max_length=80)
    condition_value: str = Field(min_length=1, max_length=255)
    action_type: Literal["NOTIFICATION", "ESCALATION", "STATUS_UPDATE"]
    action_value: str = Field(min_length=1)


class WorkflowRuleUpdate(BaseModel):
    trigger_event: str | None = Field(default=None, min_length=2, max_length=100)
    condition_type: str | None = Field(default=None, min_length=2, max_length=80)
    condition_value: str | None = Field(default=None, min_length=1, max_length=255)
    action_type: Literal["NOTIFICATION", "ESCALATION", "STATUS_UPDATE"] | None = None
    action_value: str | None = Field(default=None, min_length=1)
    is_active: bool | None = None


class WorkflowRuleRead(WorkflowRuleCreate, ORMModel):
    id: int
    workflow_id: int
    is_active: bool
    created_at: datetime


class WorkflowExecutionCreate(BaseModel):
    entity_type: Literal["TASK", "APPROVAL", "PROJECT", "MEETING"]
    entity_id: int = Field(gt=0)


class WorkflowExecutionRead(ORMModel):
    id: int
    workflow_id: int
    entity_type: str
    entity_id: int
    execution_status: str
    details: str | None = None
    executed_at: datetime


class NotificationRuleCreate(TenantScoped):
    event_type: str = Field(min_length=2, max_length=120)
    notification_type: Literal["IN_APP", "EMAIL"]
    recipient_role: str | None = Field(default=None, max_length=80)
    message_template: str | None = None


class NotificationRuleUpdate(BaseModel):
    event_type: str | None = Field(default=None, min_length=2, max_length=120)
    notification_type: Literal["IN_APP", "EMAIL"] | None = None
    recipient_role: str | None = Field(default=None, max_length=80)
    message_template: str | None = None
    is_active: bool | None = None


class NotificationRuleRead(NotificationRuleCreate, ORMModel):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class SavedSearchCreate(TenantScoped):
    user_id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=180)
    query_json: dict[str, Any]


class SavedSearchRead(SavedSearchCreate, ORMModel):
    id: int
    created_at: datetime


class KnowledgeCategoryCreate(TenantScoped):
    name: str = Field(min_length=2, max_length=180)
    description: str | None = None


class KnowledgeCategoryRead(KnowledgeCategoryCreate, ORMModel):
    id: int
    created_at: datetime


class KnowledgeArticleCreate(TenantScoped):
    category_id: int | None = Field(default=None, gt=0)
    title: str = Field(min_length=3, max_length=220)
    content: str = Field(min_length=3)
    tags: str | None = Field(default=None, max_length=500)
    created_by: int = Field(gt=0)


class KnowledgeArticleUpdate(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    title: str | None = Field(default=None, min_length=3, max_length=220)
    content: str | None = Field(default=None, min_length=3)
    tags: str | None = Field(default=None, max_length=500)
    is_archived: bool | None = None


class KnowledgeArticleRead(KnowledgeArticleCreate, ORMModel):
    id: int
    version: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime


class CustomFormCreate(TenantScoped):
    name: str = Field(min_length=2, max_length=180)
    description: str | None = None
    request_type: Literal["LEAVE", "PURCHASE", "ACCESS", "LICENSE", "OTHER"] = "OTHER"


class CustomFormUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=180)
    description: str | None = None
    request_type: Literal["LEAVE", "PURCHASE", "ACCESS", "LICENSE", "OTHER"] | None = None
    is_active: bool | None = None


class CustomFormRead(CustomFormCreate, ORMModel):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CustomFormFieldCreate(BaseModel):
    field_name: str = Field(min_length=2, max_length=160)
    field_type: Literal["TEXT", "NUMBER", "DATE", "SELECT", "FILE"]
    validation_rules: dict[str, Any] | None = None
    is_required: bool = False
    sort_order: int = Field(default=0, ge=0)


class CustomFormFieldRead(CustomFormFieldCreate, ORMModel):
    id: int
    form_id: int
    created_at: datetime
