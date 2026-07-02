from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TeamCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    name: str
    description: str | None = None
    lead_user_id: int | None = None
    created_by: int


class TeamUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    lead_user_id: int | None = None
    is_active: bool | None = None


class TeamRead(TeamCreate, ORMModel):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TeamMemberCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    team_id: int
    user_id: int
    role: str = "Member"
    allocation_percent: int = Field(default=100, ge=0, le=100)


class TeamMemberUpdate(BaseModel):
    role: str | None = None
    allocation_percent: int | None = Field(default=None, ge=0, le=100)
    is_active: bool | None = None


class TeamMemberRead(TeamMemberCreate, ORMModel):
    id: int
    is_active: bool
    joined_at: datetime


class ProjectCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    name: str
    slug: str
    description: str | None = None
    status: str = "ACTIVE"
    owner_user_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    created_by: int


class ProjectUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    status: str | None = None
    owner_user_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class ProjectRead(ProjectCreate, ORMModel):
    id: int
    created_at: datetime
    updated_at: datetime


class ProjectTeamCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    project_id: int
    team_id: int
    role: str = "Contributor"


class ProjectTeamUpdate(BaseModel):
    role: str | None = None
    is_active: bool | None = None


class ProjectTeamRead(ProjectTeamCreate, ORMModel):
    id: int
    is_active: bool
    created_at: datetime


class ProjectChannelCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    project_id: int
    name: str
    description: str | None = None
    channel_type: str = "PUBLIC"
    created_by: int


class ProjectChannelUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    channel_type: str | None = None
    is_archived: bool | None = None


class ProjectChannelRead(ProjectChannelCreate, ORMModel):
    id: int
    is_archived: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ProjectTaskCreate(BaseModel):
    title: str
    description: str | None = None
    organization_id: int
    project_id: int
    team_id: int | None = None
    assigned_to: str | None = None
    created_by: str | None = None
    priority: str = "medium"
    status: str = "todo"
    deadline: datetime | None = None


class ProjectTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    team_id: int | None = None
    assigned_to: str | None = None
    priority: str | None = None
    status: str | None = None
    deadline: datetime | None = None


class ProjectTaskRead(ProjectTaskCreate, ORMModel):
    id: int
    created_at: datetime | None = None
    completed_at: datetime | None = None
    sla_status: str | None = None
    sla_due_time: datetime | None = None
    is_sla_breached: bool | None = None


class ProjectDocumentCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    project_id: int
    title: str
    file_name: str
    file_path: str | None = None
    document_type: str = "OTHER"
    uploaded_by: int


class ProjectDocumentUpdate(BaseModel):
    title: str | None = None
    file_name: str | None = None
    file_path: str | None = None
    document_type: str | None = None


class ProjectDocumentRead(ProjectDocumentCreate, ORMModel):
    id: int
    created_at: datetime


class MeetingCreate(BaseModel):
    tenant_id: int
    workspace_id: int
    project_id: int | None = None
    team_id: int | None = None
    title: str
    agenda: str | None = None
    meeting_type: str = "PROJECT"
    location: str | None = None
    starts_at: datetime
    ends_at: datetime
    status: str = "SCHEDULED"
    created_by: int


class MeetingUpdate(BaseModel):
    project_id: int | None = None
    team_id: int | None = None
    title: str | None = None
    agenda: str | None = None
    meeting_type: str | None = None
    location: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    status: str | None = None


class MeetingRead(MeetingCreate, ORMModel):
    id: int
    created_at: datetime


class MeetingAttendeeCreate(BaseModel):
    tenant_id: int
    meeting_id: int
    user_id: int
    response_status: str = "INVITED"
    is_required: bool = True


class MeetingAttendeeUpdate(BaseModel):
    response_status: str | None = None
    is_required: bool | None = None


class MeetingAttendeeRead(MeetingAttendeeCreate, ORMModel):
    id: int
    created_at: datetime


class MeetingNoteCreate(BaseModel):
    tenant_id: int
    meeting_id: int
    author_id: int
    content: str
    decisions: str | None = None
    action_items: str | None = None


class MeetingNoteUpdate(BaseModel):
    content: str | None = None
    decisions: str | None = None
    action_items: str | None = None


class MeetingNoteRead(MeetingNoteCreate, ORMModel):
    id: int
    created_at: datetime
    updated_at: datetime


class AIMeetingSummaryRead(ORMModel):
    id: int
    tenant_id: int
    meeting_id: int
    summary: str
    key_decisions: str | None = None
    action_items: str | None = None
    generated_by: int | None = None
    created_at: datetime
