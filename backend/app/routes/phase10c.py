from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.phase10c_repository import Phase10CRepository
from app.schemas.phase10c_schema import (
    AIMeetingSummaryRead,
    MeetingAttendeeCreate,
    MeetingAttendeeRead,
    MeetingAttendeeUpdate,
    MeetingCreate,
    MeetingNoteCreate,
    MeetingNoteRead,
    MeetingNoteUpdate,
    MeetingRead,
    MeetingUpdate,
    ProjectChannelCreate,
    ProjectChannelRead,
    ProjectChannelUpdate,
    ProjectCreate,
    ProjectDocumentCreate,
    ProjectDocumentRead,
    ProjectDocumentUpdate,
    ProjectRead,
    ProjectTaskCreate,
    ProjectTaskRead,
    ProjectTaskUpdate,
    ProjectTeamCreate,
    ProjectTeamRead,
    ProjectTeamUpdate,
    ProjectUpdate,
    TeamCreate,
    TeamMemberCreate,
    TeamMemberRead,
    TeamMemberUpdate,
    TeamRead,
    TeamUpdate,
)
from app.services.phase10c_service import Phase10CService

teams_router = APIRouter(prefix="/teams", tags=["Teams"])
team_members_router = APIRouter(prefix="/team-members", tags=["Team Members"])
projects_router = APIRouter(prefix="/projects", tags=["Projects"])
project_teams_router = APIRouter(prefix="/project-teams", tags=["Project Teams"])
project_channels_router = APIRouter(prefix="/project-channels", tags=["Project Channels"])
project_tasks_router = APIRouter(prefix="/project-tasks", tags=["Project Tasks"])
project_documents_router = APIRouter(prefix="/project-documents", tags=["Project Documents"])
meetings_router = APIRouter(prefix="/meetings", tags=["Meetings"])
meeting_attendees_router = APIRouter(prefix="/meeting-attendees", tags=["Meeting Attendees"])
meeting_notes_router = APIRouter(prefix="/meeting-notes", tags=["Meeting Notes"])
ai_meeting_summary_router = APIRouter(prefix="/ai-meeting-summary", tags=["AI Meeting Summary"])
project_calendar_router = APIRouter(prefix="/project-calendar", tags=["Project Calendar"])
workload_router = APIRouter(prefix="/workload", tags=["Workload"])


def service(db: Session):
    return Phase10CService(db)


@teams_router.post("", response_model=TeamRead)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    return service(db).create_team(payload)


@teams_router.get("", response_model=Page[TeamRead])
def list_teams(
    tenant_id: int | None = None,
    workspace_id: int | None = None,
    db: Session = Depends(get_db),
):
    return paginate(db, Phase10CRepository(db).list_teams_stmt(tenant_id, workspace_id))


@teams_router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = Phase10CRepository(db).get_team(team_id)
    if not team:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@teams_router.put("/{team_id}", response_model=TeamRead)
def update_team(team_id: int, payload: TeamUpdate, db: Session = Depends(get_db)):
    return service(db).update_team(team_id, payload)


@teams_router.delete("/{team_id}")
def deactivate_team(team_id: int, db: Session = Depends(get_db)):
    return service(db).deactivate_team(team_id)


@teams_router.get("/{team_id}/members", response_model=Page[TeamMemberRead])
def list_team_members(team_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10CRepository(db).list_team_members_stmt(team_id))


@team_members_router.post("", response_model=TeamMemberRead)
def create_team_member(payload: TeamMemberCreate, db: Session = Depends(get_db)):
    return service(db).create_team_member(payload)


@team_members_router.put("/{member_id}", response_model=TeamMemberRead)
def update_team_member(member_id: int, payload: TeamMemberUpdate, db: Session = Depends(get_db)):
    return service(db).update_team_member(member_id, payload)


@team_members_router.delete("/{member_id}")
def delete_team_member(member_id: int, db: Session = Depends(get_db)):
    return service(db).delete_team_member(member_id)


@projects_router.post("", response_model=ProjectRead)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    return service(db).create_project(payload)


@projects_router.get("", response_model=Page[ProjectRead])
def list_projects(
    tenant_id: int | None = None,
    workspace_id: int | None = None,
    db: Session = Depends(get_db),
):
    return paginate(db, Phase10CRepository(db).list_projects_stmt(tenant_id, workspace_id))


@projects_router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = Phase10CRepository(db).get_project(project_id)
    if not project:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@projects_router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    return service(db).update_project(project_id, payload)


@projects_router.delete("/{project_id}")
def archive_project(project_id: int, db: Session = Depends(get_db)):
    return service(db).archive_project(project_id)


@projects_router.get("/{project_id}/teams", response_model=Page[ProjectTeamRead])
def list_project_teams(project_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10CRepository(db).list_project_teams_stmt(project_id))


@projects_router.get("/{project_id}/channels", response_model=Page[ProjectChannelRead])
def list_project_channels(project_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10CRepository(db).list_project_channels_stmt(project_id))


@projects_router.get("/{project_id}/tasks", response_model=Page[ProjectTaskRead])
def list_project_tasks(project_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10CRepository(db).list_project_tasks_stmt(project_id))


@projects_router.get("/{project_id}/documents", response_model=Page[ProjectDocumentRead])
def list_project_documents(project_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10CRepository(db).list_project_documents_stmt(project_id))


@project_teams_router.post("", response_model=ProjectTeamRead)
def create_project_team(payload: ProjectTeamCreate, db: Session = Depends(get_db)):
    return service(db).create_project_team(payload)


@project_teams_router.put("/{project_team_id}", response_model=ProjectTeamRead)
def update_project_team(project_team_id: int, payload: ProjectTeamUpdate, db: Session = Depends(get_db)):
    return service(db).update_project_team(project_team_id, payload)


@project_teams_router.delete("/{project_team_id}")
def delete_project_team(project_team_id: int, db: Session = Depends(get_db)):
    return service(db).delete_project_team(project_team_id)


@project_channels_router.post("", response_model=ProjectChannelRead)
def create_project_channel(payload: ProjectChannelCreate, db: Session = Depends(get_db)):
    return service(db).create_project_channel(payload)


@project_channels_router.put("/{channel_id}", response_model=ProjectChannelRead)
def update_project_channel(channel_id: int, payload: ProjectChannelUpdate, db: Session = Depends(get_db)):
    return service(db).update_project_channel(channel_id, payload)


@project_channels_router.delete("/{channel_id}")
def delete_project_channel(channel_id: int, db: Session = Depends(get_db)):
    return service(db).delete_project_channel(channel_id)


@project_tasks_router.post("", response_model=ProjectTaskRead)
def create_project_task(payload: ProjectTaskCreate, db: Session = Depends(get_db)):
    return service(db).create_project_task(payload)


@project_tasks_router.put("/{task_id}", response_model=ProjectTaskRead)
def update_project_task(task_id: int, payload: ProjectTaskUpdate, db: Session = Depends(get_db)):
    return service(db).update_project_task(task_id, payload)


@project_tasks_router.delete("/{task_id}")
def delete_project_task(task_id: int, db: Session = Depends(get_db)):
    return service(db).delete_project_task(task_id)


@project_documents_router.post("", response_model=ProjectDocumentRead)
def create_project_document(payload: ProjectDocumentCreate, db: Session = Depends(get_db)):
    return service(db).create_project_document(payload)


@project_documents_router.put("/{document_id}", response_model=ProjectDocumentRead)
def update_project_document(document_id: int, payload: ProjectDocumentUpdate, db: Session = Depends(get_db)):
    return service(db).update_project_document(document_id, payload)


@project_documents_router.delete("/{document_id}")
def delete_project_document(document_id: int, db: Session = Depends(get_db)):
    return service(db).delete_project_document(document_id)


@meetings_router.post("", response_model=MeetingRead)
def create_meeting(payload: MeetingCreate, db: Session = Depends(get_db)):
    return service(db).create_meeting(payload)


@meetings_router.get("", response_model=Page[MeetingRead])
def list_meetings(
    tenant_id: int | None = None,
    workspace_id: int | None = None,
    project_id: int | None = None,
    db: Session = Depends(get_db),
):
    return paginate(db, Phase10CRepository(db).list_meetings_stmt(tenant_id, workspace_id, project_id))


@meetings_router.get("/{meeting_id}", response_model=MeetingRead)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    meeting = Phase10CRepository(db).get_meeting(meeting_id)
    if not meeting:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@meetings_router.put("/{meeting_id}", response_model=MeetingRead)
def update_meeting(meeting_id: int, payload: MeetingUpdate, db: Session = Depends(get_db)):
    return service(db).update_meeting(meeting_id, payload)


@meetings_router.delete("/{meeting_id}")
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    return service(db).delete_meeting(meeting_id)


@meetings_router.get("/{meeting_id}/attendees", response_model=Page[MeetingAttendeeRead])
def list_attendees(meeting_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10CRepository(db).list_attendees_stmt(meeting_id))


@meetings_router.get("/{meeting_id}/notes", response_model=Page[MeetingNoteRead])
def list_notes(meeting_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10CRepository(db).list_notes_stmt(meeting_id))


@meeting_attendees_router.post("", response_model=MeetingAttendeeRead)
def create_attendee(payload: MeetingAttendeeCreate, db: Session = Depends(get_db)):
    return service(db).create_attendee(payload)


@meeting_attendees_router.put("/{attendee_id}", response_model=MeetingAttendeeRead)
def update_attendee(attendee_id: int, payload: MeetingAttendeeUpdate, db: Session = Depends(get_db)):
    return service(db).update_attendee(attendee_id, payload)


@meeting_attendees_router.delete("/{attendee_id}")
def delete_attendee(attendee_id: int, db: Session = Depends(get_db)):
    return service(db).delete_attendee(attendee_id)


@meeting_notes_router.post("", response_model=MeetingNoteRead)
def create_note(payload: MeetingNoteCreate, db: Session = Depends(get_db)):
    return service(db).create_note(payload)


@meeting_notes_router.put("/{note_id}", response_model=MeetingNoteRead)
def update_note(note_id: int, payload: MeetingNoteUpdate, db: Session = Depends(get_db)):
    return service(db).update_note(note_id, payload)


@meeting_notes_router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    return service(db).delete_note(note_id)


@ai_meeting_summary_router.post("/{meeting_id}", response_model=AIMeetingSummaryRead)
def generate_ai_summary(
    meeting_id: int,
    generated_by: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return service(db).generate_ai_summary(meeting_id, generated_by)


@ai_meeting_summary_router.get("/{meeting_id}", response_model=AIMeetingSummaryRead)
def get_ai_summary(meeting_id: int, db: Session = Depends(get_db)):
    summary = Phase10CRepository(db).get_ai_summary(meeting_id)
    if not summary:
        return service(db).generate_ai_summary(meeting_id)
    return summary


@project_calendar_router.get("/{project_id}")
def project_calendar(
    project_id: int,
    start: datetime | None = None,
    end: datetime | None = None,
    db: Session = Depends(get_db),
):
    repo = Phase10CRepository(db)
    if repo.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    def database_datetime(value: datetime | None):
        if value is None or value.tzinfo is None:
            return value
        return value.astimezone(timezone.utc).replace(tzinfo=None)

    start = database_datetime(start)
    end = database_datetime(end)
    if start is not None and end is not None and start > end:
        raise HTTPException(
            status_code=400,
            detail="Calendar start must be before or equal to end",
        )

    meetings_stmt = repo.list_meetings_stmt(project_id=project_id)
    tasks_stmt = repo.list_project_tasks_stmt(project_id)
    meetings = db.execute(meetings_stmt).scalars().all()
    tasks = db.execute(tasks_stmt).scalars().all()
    if start is not None:
        meetings = [item for item in meetings if item.starts_at >= start]
        tasks = [item for item in tasks if item.deadline is None or item.deadline >= start]
    if end is not None:
        meetings = [item for item in meetings if item.starts_at <= end]
        tasks = [item for item in tasks if item.deadline is None or item.deadline <= end]
    return {
        "project_id": project_id,
        "events": [
            {
                "id": f"meeting-{meeting.id}",
                "type": "meeting",
                "title": meeting.title,
                "starts_at": meeting.starts_at,
                "ends_at": meeting.ends_at,
                "status": meeting.status,
            }
            for meeting in meetings
        ]
        + [
            {
                "id": f"task-{task.id}",
                "type": "task",
                "title": task.title,
                "starts_at": task.deadline,
                "ends_at": task.deadline,
                "status": task.status,
            }
            for task in tasks
        ],
    }


@workload_router.get("/teams/{team_id}")
def team_workload(team_id: int, db: Session = Depends(get_db)):
    return Phase10CRepository(db).team_workload(team_id)


@workload_router.get("/projects/{project_id}")
def project_workload(project_id: int, db: Session = Depends(get_db)):
    return Phase10CRepository(db).project_workload(project_id)
