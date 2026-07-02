from fastapi import HTTPException
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError

from app.models.channel import Channel
from app.models.organization import Organization
from app.models.phase10c import (
    AIMeetingSummary,
    Meeting,
    MeetingAttendee,
    MeetingNote,
    Project,
    ProjectDocument,
    ProjectTeam,
    Team,
    TeamMember,
)
from app.models.task import Task
from app.models.user import User
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember


class Phase10CRepository:
    def __init__(self, db):
        self.db = db

    def get_tenant(self, tenant_id: int):
        return self.db.execute(select(Organization).where(Organization.id == tenant_id)).scalar_one_or_none()

    def get_workspace(self, workspace_id: int):
        return self.db.execute(select(Workspace).where(Workspace.id == workspace_id)).scalar_one_or_none()

    def get_user(self, user_id: int):
        return self.db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    def get_active_workspace_member(self, workspace_id: int, user_id: int):
        return self.db.execute(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == user_id,
                WorkspaceMember.is_active.is_(True),
            )
        ).scalar_one_or_none()

    def get_team(self, team_id: int):
        return self.db.execute(select(Team).where(Team.id == team_id)).scalar_one_or_none()

    def get_project(self, project_id: int):
        return self.db.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()

    def get_meeting(self, meeting_id: int):
        return self.db.execute(select(Meeting).where(Meeting.id == meeting_id)).scalar_one_or_none()

    def get_channel(self, channel_id: int):
        return self.db.execute(select(Channel).where(Channel.id == channel_id)).scalar_one_or_none()

    def get_task(self, task_id: int):
        return self.db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()

    def add(self, entity):
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status_code=409, detail="Record conflicts with existing data") from exc

    def delete(self, entity):
        try:
            self.db.delete(entity)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status_code=409, detail="Record is still in use") from exc

    def delete_meeting_graph(self, meeting_id: int):
        try:
            self.db.execute(delete(AIMeetingSummary).where(AIMeetingSummary.meeting_id == meeting_id))
            self.db.execute(delete(MeetingNote).where(MeetingNote.meeting_id == meeting_id))
            self.db.execute(delete(MeetingAttendee).where(MeetingAttendee.meeting_id == meeting_id))
            self.db.execute(delete(Meeting).where(Meeting.id == meeting_id))
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status_code=409, detail="Meeting is still in use") from exc

    def list_teams_stmt(self, tenant_id: int | None = None, workspace_id: int | None = None):
        stmt = select(Team).order_by(Team.created_at.desc())
        if tenant_id is not None:
            stmt = stmt.where(Team.tenant_id == tenant_id)
        if workspace_id is not None:
            stmt = stmt.where(Team.workspace_id == workspace_id)
        return stmt

    def list_team_members_stmt(self, team_id: int):
        return select(TeamMember).where(TeamMember.team_id == team_id).order_by(TeamMember.joined_at.desc())

    def get_team_member(self, member_id: int):
        return self.db.execute(select(TeamMember).where(TeamMember.id == member_id)).scalar_one_or_none()

    def get_team_member_by_user(self, team_id: int, user_id: int):
        return self.db.execute(
            select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == user_id)
        ).scalar_one_or_none()

    def list_projects_stmt(self, tenant_id: int | None = None, workspace_id: int | None = None):
        stmt = select(Project).order_by(Project.created_at.desc())
        if tenant_id is not None:
            stmt = stmt.where(Project.tenant_id == tenant_id)
        if workspace_id is not None:
            stmt = stmt.where(Project.workspace_id == workspace_id)
        return stmt

    def get_project_team(self, project_team_id: int):
        return self.db.execute(select(ProjectTeam).where(ProjectTeam.id == project_team_id)).scalar_one_or_none()

    def get_project_team_by_pair(self, project_id: int, team_id: int):
        return self.db.execute(
            select(ProjectTeam).where(ProjectTeam.project_id == project_id, ProjectTeam.team_id == team_id)
        ).scalar_one_or_none()

    def list_project_teams_stmt(self, project_id: int):
        return select(ProjectTeam).where(ProjectTeam.project_id == project_id).order_by(ProjectTeam.created_at.desc())

    def list_project_channels_stmt(self, project_id: int):
        return select(Channel).where(Channel.project_id == project_id).order_by(Channel.created_at.desc())

    def list_project_tasks_stmt(self, project_id: int):
        return select(Task).where(Task.project_id == project_id).order_by(Task.created_at.desc())

    def list_project_documents_stmt(self, project_id: int):
        return select(ProjectDocument).where(ProjectDocument.project_id == project_id).order_by(ProjectDocument.created_at.desc())

    def get_project_document(self, document_id: int):
        return self.db.execute(select(ProjectDocument).where(ProjectDocument.id == document_id)).scalar_one_or_none()

    def list_meetings_stmt(self, tenant_id: int | None = None, workspace_id: int | None = None, project_id: int | None = None):
        stmt = select(Meeting).order_by(Meeting.starts_at.asc())
        if tenant_id is not None:
            stmt = stmt.where(Meeting.tenant_id == tenant_id)
        if workspace_id is not None:
            stmt = stmt.where(Meeting.workspace_id == workspace_id)
        if project_id is not None:
            stmt = stmt.where(Meeting.project_id == project_id)
        return stmt

    def get_attendee(self, attendee_id: int):
        return self.db.execute(select(MeetingAttendee).where(MeetingAttendee.id == attendee_id)).scalar_one_or_none()

    def get_attendee_by_user(self, meeting_id: int, user_id: int):
        return self.db.execute(
            select(MeetingAttendee).where(MeetingAttendee.meeting_id == meeting_id, MeetingAttendee.user_id == user_id)
        ).scalar_one_or_none()

    def list_attendees_stmt(self, meeting_id: int):
        return select(MeetingAttendee).where(MeetingAttendee.meeting_id == meeting_id).order_by(MeetingAttendee.created_at.desc())

    def get_note(self, note_id: int):
        return self.db.execute(select(MeetingNote).where(MeetingNote.id == note_id)).scalar_one_or_none()

    def list_notes_stmt(self, meeting_id: int):
        return select(MeetingNote).where(MeetingNote.meeting_id == meeting_id).order_by(MeetingNote.created_at.desc())

    def get_ai_summary(self, meeting_id: int):
        return self.db.execute(select(AIMeetingSummary).where(AIMeetingSummary.meeting_id == meeting_id)).scalar_one_or_none()

    def team_workload(self, team_id: int):
        status_rows = self.db.execute(
            select(Task.status, func.count(Task.id)).where(Task.team_id == team_id).group_by(Task.status)
        ).all()
        members = self.db.execute(
            select(func.count(TeamMember.id)).where(TeamMember.team_id == team_id, TeamMember.is_active.is_(True))
        ).scalar_one()
        return {
            "team_id": team_id,
            "active_members": members,
            "tasks_by_status": {status or "unknown": count for status, count in status_rows},
            "total_tasks": sum(count for _, count in status_rows),
        }

    def project_workload(self, project_id: int):
        status_rows = self.db.execute(
            select(Task.status, func.count(Task.id)).where(Task.project_id == project_id).group_by(Task.status)
        ).all()
        team_rows = self.db.execute(
            select(Task.team_id, func.count(Task.id)).where(Task.project_id == project_id).group_by(Task.team_id)
        ).all()
        return {
            "project_id": project_id,
            "tasks_by_status": {status or "unknown": count for status, count in status_rows},
            "tasks_by_team": {str(team_id or "unassigned"): count for team_id, count in team_rows},
            "total_tasks": sum(count for _, count in status_rows),
        }
