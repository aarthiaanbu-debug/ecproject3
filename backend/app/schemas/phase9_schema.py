from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class SLARuleBase(BaseModel):
    module_name: str
    priority: str
    allowed_hours: int = Field(gt=0)
    escalation_enabled: bool = False
    escalation_after_hours: int = Field(default=0, ge=0)
    is_active: bool = True
    created_by: Optional[int] = None


class SLARuleCreate(SLARuleBase):
    pass


class SLARuleUpdate(BaseModel):
    module_name: Optional[str] = None
    priority: Optional[str] = None
    allowed_hours: Optional[int] = Field(default=None, gt=0)
    escalation_enabled: Optional[bool] = None
    escalation_after_hours: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class EscalationCreate(BaseModel):
    approval_id: int
    escalated_from: Optional[int] = None
    escalated_to: int
    reason: str
    escalation_level: int = Field(default=1, ge=1)


class DelegationCreate(BaseModel):
    delegator_id: int
    delegatee_id: int
    start_date: datetime
    end_date: datetime
    reason: str

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        return self


class NotificationPreferenceUpdate(BaseModel):
    in_app_enabled: bool = True
    email_enabled: bool = False
    task_notifications: bool = True
    approval_notifications: bool = True
    escalation_notifications: bool = True
    document_notifications: bool = True
