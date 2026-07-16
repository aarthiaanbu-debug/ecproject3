from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError

from app.models.approval import Approval
from app.models.audit import AuditLog
from app.models.channel_message import ChannelMessage
from app.models.document import Document
from app.models.notification import Notification
from app.models.phase10c import Meeting, MeetingNote, Project, ProjectDocument, Team, TeamMember
from app.models.phase10d import (
    CustomForm,
    CustomFormField,
    KnowledgeArticle,
    KnowledgeCategory,
    NotificationRule,
    SavedSearch,
    WorkflowDefinition,
    WorkflowExecution,
    WorkflowRule,
)
from app.models.task import Task
from app.models.user import User
from app.models.workspace_message import WorkspaceMessage


class Phase10DRepository:
    def __init__(self, db):
        self.db = db

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

    def get_workflow(self, workflow_id: int):
        return self.db.execute(select(WorkflowDefinition).where(WorkflowDefinition.id == workflow_id)).scalar_one_or_none()

    def list_workflows_stmt(self, tenant_id: int | None = None):
        stmt = select(WorkflowDefinition).order_by(WorkflowDefinition.created_at.desc())
        if tenant_id is not None:
            stmt = stmt.where(WorkflowDefinition.tenant_id == tenant_id)
        return stmt

    def get_rule(self, rule_id: int):
        return self.db.execute(select(WorkflowRule).where(WorkflowRule.id == rule_id)).scalar_one_or_none()

    def list_rules_stmt(self, workflow_id: int):
        return select(WorkflowRule).where(WorkflowRule.workflow_id == workflow_id).order_by(WorkflowRule.created_at.desc())

    def list_executions_stmt(self, workflow_id: int):
        return (
            select(WorkflowExecution)
            .where(WorkflowExecution.workflow_id == workflow_id)
            .order_by(WorkflowExecution.executed_at.desc())
        )

    def get_notification_rule(self, rule_id: int):
        return self.db.execute(select(NotificationRule).where(NotificationRule.id == rule_id)).scalar_one_or_none()

    def list_notification_rules_stmt(self, tenant_id: int | None = None):
        stmt = select(NotificationRule).order_by(NotificationRule.created_at.desc())
        if tenant_id is not None:
            stmt = stmt.where(NotificationRule.tenant_id == tenant_id)
        return stmt

    def list_saved_searches_stmt(self, tenant_id: int | None = None, user_id: int | None = None):
        stmt = select(SavedSearch).order_by(SavedSearch.created_at.desc())
        if tenant_id is not None:
            stmt = stmt.where(SavedSearch.tenant_id == tenant_id)
        if user_id is not None:
            stmt = stmt.where(SavedSearch.user_id == user_id)
        return stmt

    def get_saved_search(self, search_id: int):
        return self.db.execute(select(SavedSearch).where(SavedSearch.id == search_id)).scalar_one_or_none()

    def list_categories_stmt(self, tenant_id: int | None = None):
        stmt = select(KnowledgeCategory).order_by(KnowledgeCategory.name.asc())
        if tenant_id is not None:
            stmt = stmt.where(KnowledgeCategory.tenant_id == tenant_id)
        return stmt

    def get_category(self, category_id: int):
        return self.db.execute(select(KnowledgeCategory).where(KnowledgeCategory.id == category_id)).scalar_one_or_none()

    def get_article(self, article_id: int):
        return self.db.execute(select(KnowledgeArticle).where(KnowledgeArticle.id == article_id)).scalar_one_or_none()

    def list_articles_stmt(self, tenant_id: int | None = None, category_id: int | None = None, q: str | None = None):
        stmt = select(KnowledgeArticle).where(KnowledgeArticle.is_archived.is_(False)).order_by(KnowledgeArticle.updated_at.desc())
        if tenant_id is not None:
            stmt = stmt.where(KnowledgeArticle.tenant_id == tenant_id)
        if category_id is not None:
            stmt = stmt.where(KnowledgeArticle.category_id == category_id)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(or_(KnowledgeArticle.title.ilike(like), KnowledgeArticle.content.ilike(like), KnowledgeArticle.tags.ilike(like)))
        return stmt

    def get_form(self, form_id: int):
        return self.db.execute(select(CustomForm).where(CustomForm.id == form_id)).scalar_one_or_none()

    def list_forms_stmt(self, tenant_id: int | None = None):
        stmt = select(CustomForm).order_by(CustomForm.created_at.desc())
        if tenant_id is not None:
            stmt = stmt.where(CustomForm.tenant_id == tenant_id)
        return stmt

    def list_fields_stmt(self, form_id: int):
        return select(CustomFormField).where(CustomFormField.form_id == form_id).order_by(CustomFormField.sort_order.asc(), CustomFormField.id.asc())

    def audit(self, action: str, module_name: str, record_id: int | None = None, user_id: int | None = None, details: str | None = None):
        log = AuditLog(
            action=action,
            action_type=action,
            module_name=module_name,
            record_id=record_id,
            user_id=user_id,
            user="System" if user_id is None else str(user_id),
            details=details,
        )
        self.db.add(log)
        self.db.commit()
        return log

    def search_projects(self, tenant_id: int, q: str):
        like = f"%{q}%"
        return self.db.execute(
            select(Project).where(Project.tenant_id == tenant_id, or_(Project.name.ilike(like), Project.description.ilike(like))).limit(20)
        ).scalars().all()

    def search_users(self, tenant_id: int, q: str):
        like = f"%{q}%"
        return self.db.execute(
            select(User).where(User.organization_id == tenant_id, or_(User.name.ilike(like), User.email.ilike(like))).limit(20)
        ).scalars().all()

    def search_teams(self, tenant_id: int, q: str):
        like = f"%{q}%"
        return self.db.execute(
            select(Team).where(Team.tenant_id == tenant_id, or_(Team.name.ilike(like), Team.description.ilike(like))).limit(20)
        ).scalars().all()

    def search_tasks(self, tenant_id: int, q: str):
        like = f"%{q}%"
        return self.db.execute(
            select(Task).where(Task.organization_id == tenant_id, or_(Task.title.ilike(like), Task.description.ilike(like))).limit(20)
        ).scalars().all()

    def search_documents(self, tenant_id: int, q: str):
        like = f"%{q}%"
        project_docs = self.db.execute(
            select(ProjectDocument).where(ProjectDocument.tenant_id == tenant_id, ProjectDocument.title.ilike(like)).limit(20)
        ).scalars().all()
        docs = self.db.execute(select(Document).where(Document.file_name.ilike(like)).limit(20)).scalars().all()
        return project_docs, docs

    def search_messages(self, tenant_id: int, q: str):
        like = f"%{q}%"
        workspace = self.db.execute(
            select(WorkspaceMessage).where(WorkspaceMessage.tenant_id == tenant_id, WorkspaceMessage.message.ilike(like)).limit(20)
        ).scalars().all()
        channel = self.db.execute(
            select(ChannelMessage).where(ChannelMessage.tenant_id == tenant_id, ChannelMessage.content.ilike(like)).limit(20)
        ).scalars().all()
        return workspace, channel

    def search_meetings(self, tenant_id: int, q: str):
        like = f"%{q}%"
        meetings = self.db.execute(
            select(Meeting).where(Meeting.tenant_id == tenant_id, or_(Meeting.title.ilike(like), Meeting.agenda.ilike(like))).limit(20)
        ).scalars().all()
        notes = self.db.execute(
            select(MeetingNote).where(MeetingNote.tenant_id == tenant_id, MeetingNote.content.ilike(like)).limit(20)
        ).scalars().all()
        return meetings, notes

    def search_approvals(self, tenant_id: int, q: str):
        like = f"%{q}%"
        task_ids = select(Task.id).where(Task.organization_id == tenant_id)
        return self.db.execute(
            select(Approval).where(Approval.task_id.in_(task_ids), Approval.status.ilike(like)).limit(20)
        ).scalars().all()

    def analytics_counts(self, tenant_id: int | None = None):
        task_stmt = select(Task.status, func.count(Task.id)).group_by(Task.status)
        if tenant_id is not None:
            task_stmt = task_stmt.where(Task.organization_id == tenant_id)
        return self.db.execute(task_stmt).all()

    def project_analytics(self, tenant_id: int | None = None):
        stmt = select(Project.status, func.count(Project.id)).group_by(Project.status)
        if tenant_id is not None:
            stmt = stmt.where(Project.tenant_id == tenant_id)
        return self.db.execute(stmt).all()

    def team_analytics(self, tenant_id: int | None = None):
        stmt = select(Team.id, Team.name, func.count(TeamMember.id)).join(TeamMember, TeamMember.team_id == Team.id, isouter=True).group_by(Team.id, Team.name)
        if tenant_id is not None:
            stmt = stmt.where(Team.tenant_id == tenant_id)
        return self.db.execute(stmt).all()

    def approval_analytics(self):
        return self.db.execute(select(Approval.status, func.count(Approval.id)).group_by(Approval.status)).all()

    def document_analytics(self):
        return {
            "documents": self.db.execute(select(func.count(Document.id))).scalar_one(),
            "project_documents": self.db.execute(select(func.count(ProjectDocument.id))).scalar_one(),
        }

    def recent_report_rows(self, kind: str, tenant_id: int | None = None):
        models = {
            "projects": Project,
            "tasks": Task,
            "approvals": Approval,
            "documents": ProjectDocument,
        }
        model = models[kind]
        stmt = select(model).limit(200)
        if tenant_id is not None and hasattr(model, "tenant_id"):
            stmt = stmt.where(model.tenant_id == tenant_id)
        if tenant_id is not None and model is Task:
            stmt = stmt.where(Task.organization_id == tenant_id)
        return self.db.execute(stmt).scalars().all()
