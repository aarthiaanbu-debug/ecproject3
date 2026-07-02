from fastapi import HTTPException

from app.models.channel import Channel
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
from app.repositories.phase10c_repository import Phase10CRepository


class Phase10CService:
    def __init__(self, db):
        self.repo = Phase10CRepository(db)

    def _require_tenant(self, tenant_id: int):
        tenant = self.repo.get_tenant(tenant_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        return tenant

    def _require_workspace(self, workspace_id: int, tenant_id: int):
        workspace = self.repo.get_workspace(workspace_id)
        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace not found")
        if workspace.tenant_id != tenant_id:
            raise HTTPException(status_code=403, detail="Workspace does not belong to tenant")
        return workspace

    def _require_team(self, team_id: int, tenant_id: int, workspace_id: int | None = None):
        team = self.repo.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        if team.tenant_id != tenant_id:
            raise HTTPException(status_code=403, detail="Team does not belong to tenant")
        if workspace_id is not None and team.workspace_id != workspace_id:
            raise HTTPException(status_code=403, detail="Team does not belong to workspace")
        return team

    def _require_project(self, project_id: int, tenant_id: int, workspace_id: int | None = None):
        project = self.repo.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project.tenant_id != tenant_id:
            raise HTTPException(status_code=403, detail="Project does not belong to tenant")
        if workspace_id is not None and project.workspace_id != workspace_id:
            raise HTTPException(status_code=403, detail="Project does not belong to workspace")
        return project

    def _require_meeting(self, meeting_id: int, tenant_id: int | None = None):
        meeting = self.repo.get_meeting(meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        if tenant_id is not None and meeting.tenant_id != tenant_id:
            raise HTTPException(status_code=403, detail="Meeting does not belong to tenant")
        return meeting

    def _validate_user_tenant(
        self,
        user_id: int | None,
        tenant_id: int,
        field_name: str = "user_id",
        workspace_id: int | None = None,
    ):
        if user_id is None:
            return
        user = self.repo.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        belongs_to_tenant = user.organization_id in (None, tenant_id)
        belongs_to_workspace = (
            workspace_id is not None
            and self.repo.get_active_workspace_member(workspace_id, user_id) is not None
        )
        if not belongs_to_tenant and not belongs_to_workspace:
            raise HTTPException(
                status_code=403,
                detail=(
                    f"{field_name} user {user_id} does not belong to tenant "
                    f"{tenant_id}"
                ),
            )

    def create_team(self, data):
        self._require_tenant(data.tenant_id)
        self._require_workspace(data.workspace_id, data.tenant_id)
        self._validate_user_tenant(
            data.lead_user_id,
            data.tenant_id,
            "lead_user_id",
            data.workspace_id,
        )
        self._validate_user_tenant(
            data.created_by,
            data.tenant_id,
            "created_by",
            data.workspace_id,
        )
        return self.repo.add(Team(**data.model_dump()))

    def update_team(self, team_id: int, data):
        team = self.repo.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        values = data.model_dump(exclude_unset=True)
        if "lead_user_id" in values:
            self._validate_user_tenant(
                values["lead_user_id"],
                team.tenant_id,
                "lead_user_id",
                team.workspace_id,
            )
        for key, value in values.items():
            setattr(team, key, value)
        return self.repo.add(team)

    def deactivate_team(self, team_id: int):
        team = self.repo.get_team(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        team.is_active = False
        self.repo.add(team)
        return {"message": "Team deactivated"}

    def create_team_member(self, data):
        self._require_workspace(data.workspace_id, data.tenant_id)
        self._require_team(data.team_id, data.tenant_id, data.workspace_id)
        self._validate_user_tenant(
            data.user_id,
            data.tenant_id,
            "user_id",
            data.workspace_id,
        )
        existing = self.repo.get_team_member_by_user(data.team_id, data.user_id)
        if existing:
            existing.role = data.role
            existing.allocation_percent = data.allocation_percent
            existing.is_active = True
            return self.repo.add(existing)
        return self.repo.add(TeamMember(**data.model_dump()))

    def update_team_member(self, member_id: int, data):
        member = self.repo.get_team_member(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Team member not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(member, key, value)
        return self.repo.add(member)

    def delete_team_member(self, member_id: int):
        member = self.repo.get_team_member(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Team member not found")
        self.repo.delete(member)
        return {"message": "Team member removed"}

    def create_project(self, data):
        self._require_tenant(data.tenant_id)
        self._require_workspace(data.workspace_id, data.tenant_id)
        self._validate_user_tenant(
            data.owner_user_id,
            data.tenant_id,
            "owner_user_id",
            data.workspace_id,
        )
        self._validate_user_tenant(
            data.created_by,
            data.tenant_id,
            "created_by",
            data.workspace_id,
        )
        return self.repo.add(Project(**data.model_dump()))

    def update_project(self, project_id: int, data):
        project = self.repo.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        values = data.model_dump(exclude_unset=True)
        if "owner_user_id" in values:
            self._validate_user_tenant(
                values["owner_user_id"],
                project.tenant_id,
                "owner_user_id",
                project.workspace_id,
            )
        for key, value in values.items():
            setattr(project, key, value)
        return self.repo.add(project)

    def archive_project(self, project_id: int):
        project = self.repo.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        project.status = "ARCHIVED"
        self.repo.add(project)
        return {"message": "Project archived"}

    def create_project_team(self, data):
        self._require_workspace(data.workspace_id, data.tenant_id)
        self._require_project(data.project_id, data.tenant_id, data.workspace_id)
        self._require_team(data.team_id, data.tenant_id, data.workspace_id)
        existing = self.repo.get_project_team_by_pair(data.project_id, data.team_id)
        if existing:
            existing.role = data.role
            existing.is_active = True
            return self.repo.add(existing)
        return self.repo.add(ProjectTeam(**data.model_dump()))

    def update_project_team(self, project_team_id: int, data):
        project_team = self.repo.get_project_team(project_team_id)
        if not project_team:
            raise HTTPException(status_code=404, detail="Project team not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(project_team, key, value)
        return self.repo.add(project_team)

    def delete_project_team(self, project_team_id: int):
        project_team = self.repo.get_project_team(project_team_id)
        if not project_team:
            raise HTTPException(status_code=404, detail="Project team not found")
        self.repo.delete(project_team)
        return {"message": "Project team removed"}

    def create_project_channel(self, data):
        self._require_project(data.project_id, data.tenant_id, data.workspace_id)
        self._validate_user_tenant(
            data.created_by,
            data.tenant_id,
            "created_by",
            data.workspace_id,
        )
        return self.repo.add(Channel(**data.model_dump()))

    def update_project_channel(self, channel_id: int, data):
        channel = self.repo.get_channel(channel_id)
        if not channel or channel.project_id is None:
            raise HTTPException(status_code=404, detail="Project channel not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(channel, key, value)
        return self.repo.add(channel)

    def delete_project_channel(self, channel_id: int):
        channel = self.repo.get_channel(channel_id)
        if not channel or channel.project_id is None:
            raise HTTPException(status_code=404, detail="Project channel not found")
        self.repo.delete(channel)
        return {"message": "Project channel deleted"}

    def create_project_task(self, data):
        project = self._require_project(data.project_id, data.organization_id)
        if data.team_id is not None:
            self._require_team(data.team_id, data.organization_id, project.workspace_id)
        return self.repo.add(Task(**data.model_dump()))

    def update_project_task(self, task_id: int, data):
        task = self.repo.get_task(task_id)
        if not task or task.project_id is None:
            raise HTTPException(status_code=404, detail="Project task not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        return self.repo.add(task)

    def delete_project_task(self, task_id: int):
        task = self.repo.get_task(task_id)
        if not task or task.project_id is None:
            raise HTTPException(status_code=404, detail="Project task not found")
        self.repo.delete(task)
        return {"message": "Project task deleted"}

    def create_project_document(self, data):
        self._require_project(data.project_id, data.tenant_id, data.workspace_id)
        self._validate_user_tenant(
            data.uploaded_by,
            data.tenant_id,
            "uploaded_by",
            data.workspace_id,
        )
        return self.repo.add(ProjectDocument(**data.model_dump()))

    def update_project_document(self, document_id: int, data):
        document = self.repo.get_project_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Project document not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(document, key, value)
        return self.repo.add(document)

    def delete_project_document(self, document_id: int):
        document = self.repo.get_project_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Project document not found")
        self.repo.delete(document)
        return {"message": "Project document deleted"}

    def create_meeting(self, data):
        self._require_workspace(data.workspace_id, data.tenant_id)
        if data.project_id is not None:
            self._require_project(data.project_id, data.tenant_id, data.workspace_id)
        if data.team_id is not None:
            self._require_team(data.team_id, data.tenant_id, data.workspace_id)
        self._validate_user_tenant(
            data.created_by,
            data.tenant_id,
            "created_by",
            data.workspace_id,
        )
        if data.ends_at <= data.starts_at:
            raise HTTPException(status_code=400, detail="Meeting end time must be after start time")
        return self.repo.add(Meeting(**data.model_dump()))

    def update_meeting(self, meeting_id: int, data):
        meeting = self._require_meeting(meeting_id)
        values = data.model_dump(exclude_unset=True)
        project_id = values.get("project_id", meeting.project_id)
        team_id = values.get("team_id", meeting.team_id)
        if project_id is not None:
            self._require_project(project_id, meeting.tenant_id, meeting.workspace_id)
        if team_id is not None:
            self._require_team(team_id, meeting.tenant_id, meeting.workspace_id)
        for key, value in values.items():
            setattr(meeting, key, value)
        if meeting.ends_at <= meeting.starts_at:
            raise HTTPException(status_code=400, detail="Meeting end time must be after start time")
        return self.repo.add(meeting)

    def delete_meeting(self, meeting_id: int):
        self._require_meeting(meeting_id)
        self.repo.delete_meeting_graph(meeting_id)
        return {"message": "Meeting deleted"}

    def create_attendee(self, data):
        meeting = self._require_meeting(data.meeting_id, data.tenant_id)
        self._validate_user_tenant(
            data.user_id,
            meeting.tenant_id,
            "user_id",
            meeting.workspace_id,
        )
        existing = self.repo.get_attendee_by_user(data.meeting_id, data.user_id)
        if existing:
            existing.response_status = data.response_status
            existing.is_required = data.is_required
            return self.repo.add(existing)
        return self.repo.add(MeetingAttendee(**data.model_dump()))

    def update_attendee(self, attendee_id: int, data):
        attendee = self.repo.get_attendee(attendee_id)
        if not attendee:
            raise HTTPException(status_code=404, detail="Meeting attendee not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(attendee, key, value)
        return self.repo.add(attendee)

    def delete_attendee(self, attendee_id: int):
        attendee = self.repo.get_attendee(attendee_id)
        if not attendee:
            raise HTTPException(status_code=404, detail="Meeting attendee not found")
        self.repo.delete(attendee)
        return {"message": "Meeting attendee removed"}

    def create_note(self, data):
        meeting = self._require_meeting(data.meeting_id, data.tenant_id)
        self._validate_user_tenant(
            data.author_id,
            meeting.tenant_id,
            "author_id",
            meeting.workspace_id,
        )
        return self.repo.add(MeetingNote(**data.model_dump()))

    def update_note(self, note_id: int, data):
        note = self.repo.get_note(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Meeting note not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(note, key, value)
        return self.repo.add(note)

    def delete_note(self, note_id: int):
        note = self.repo.get_note(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Meeting note not found")
        self.repo.delete(note)
        return {"message": "Meeting note deleted"}

    def generate_ai_summary(self, meeting_id: int, generated_by: int | None = None):
        meeting = self._require_meeting(meeting_id)
        self._validate_user_tenant(
            generated_by,
            meeting.tenant_id,
            "generated_by",
            meeting.workspace_id,
        )
        notes = self.repo.db.execute(self.repo.list_notes_stmt(meeting_id)).scalars().all()
        content = " ".join(note.content for note in notes) or meeting.agenda or "No notes have been captured yet."
        decisions = "\n".join(note.decisions for note in notes if note.decisions) or "No decisions recorded."
        action_items = "\n".join(note.action_items for note in notes if note.action_items) or "No action items recorded."
        summary_text = f"{meeting.title}: {content[:700]}"
        summary = self.repo.get_ai_summary(meeting_id)
        if summary:
            summary.summary = summary_text
            summary.key_decisions = decisions
            summary.action_items = action_items
            summary.generated_by = generated_by
            return self.repo.add(summary)
        return self.repo.add(
            AIMeetingSummary(
                tenant_id=meeting.tenant_id,
                meeting_id=meeting_id,
                summary=summary_text,
                key_decisions=decisions,
                action_items=action_items,
                generated_by=generated_by,
            )
        )
