import json
from datetime import datetime

from fastapi import HTTPException

from app.cache.redis_cache import redis_client
from app.models.notification import Notification
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
from app.repositories.phase10d_repository import Phase10DRepository


class Phase10DService:
    def __init__(self, db):
        self.repo = Phase10DRepository(db)

    def _require_same_tenant(self, entity, tenant_id: int):
        if getattr(entity, "tenant_id", tenant_id) != tenant_id:
            raise HTTPException(status_code=403, detail="Cross tenant access denied")

    def create_workflow(self, data, user_id: int | None = None):
        workflow = self.repo.add(WorkflowDefinition(**data.model_dump()))
        self.repo.audit("CREATE", "workflow_definitions", workflow.id, user_id, f"Workflow {workflow.name} created")
        return workflow

    def update_workflow(self, workflow_id: int, data, user_id: int | None = None):
        workflow = self.repo.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(workflow, key, value)
        workflow = self.repo.add(workflow)
        self.repo.audit("UPDATE", "workflow_definitions", workflow.id, user_id)
        return workflow

    def disable_workflow(self, workflow_id: int, user_id: int | None = None):
        workflow = self.repo.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        workflow.is_active = False
        self.repo.add(workflow)
        self.repo.audit("DISABLE", "workflow_definitions", workflow.id, user_id)
        return {"message": "Workflow disabled"}

    def add_workflow_rule(self, workflow_id: int, data, user_id: int | None = None):
        workflow = self.repo.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        rule = self.repo.add(WorkflowRule(workflow_id=workflow_id, **data.model_dump()))
        self.repo.audit("CREATE", "workflow_rules", rule.id, user_id)
        return rule

    def execute_workflow(self, workflow_id: int, data, user_id: int | None = None):
        workflow = self.repo.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        if not workflow.is_active:
            raise HTTPException(status_code=400, detail="Workflow is disabled")
        rules = self.repo.db.execute(self.repo.list_rules_stmt(workflow_id)).scalars().all()
        details = f"Evaluated {len(rules)} active rules for {data.entity_type} #{data.entity_id}"
        execution = self.repo.add(
            WorkflowExecution(
                workflow_id=workflow_id,
                entity_type=data.entity_type,
                entity_id=data.entity_id,
                execution_status="SUCCESS",
                details=details,
            )
        )
        for rule in rules:
            if rule.is_active and rule.action_type == "NOTIFICATION":
                self.repo.db.add(
                    Notification(
                        user_id=user_id,
                        message=rule.action_value[:250],
                        notification_type="workflow",
                        priority="normal",
                    )
                )
        self.repo.db.commit()
        self.repo.audit("EXECUTE", "workflow_executions", execution.id, user_id, details)
        return execution

    def create_notification_rule(self, data, user_id: int | None = None):
        rule = self.repo.add(NotificationRule(**data.model_dump()))
        self.repo.audit("CREATE", "notification_rules", rule.id, user_id)
        return rule

    def update_notification_rule(self, rule_id: int, data, user_id: int | None = None):
        rule = self.repo.get_notification_rule(rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail="Notification rule not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(rule, key, value)
        rule = self.repo.add(rule)
        self.repo.audit("UPDATE", "notification_rules", rule.id, user_id)
        return rule

    def disable_notification_rule(self, rule_id: int, user_id: int | None = None):
        rule = self.repo.get_notification_rule(rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail="Notification rule not found")
        rule.is_active = False
        self.repo.add(rule)
        self.repo.audit("DISABLE", "notification_rules", rule.id, user_id)
        return {"message": "Notification rule disabled"}

    def save_search(self, data, user_id: int | None = None):
        saved = self.repo.add(SavedSearch(**data.model_dump()))
        self.repo.audit("CREATE", "saved_searches", saved.id, user_id or data.user_id)
        return saved

    def delete_saved_search(self, search_id: int, user_id: int | None = None):
        saved = self.repo.get_saved_search(search_id)
        if not saved:
            raise HTTPException(status_code=404, detail="Saved search not found")
        self.repo.delete(saved)
        self.repo.audit("DELETE", "saved_searches", search_id, user_id)
        return {"message": "Saved search deleted"}

    def create_category(self, data, user_id: int | None = None):
        category = self.repo.add(KnowledgeCategory(**data.model_dump()))
        self.repo.audit("CREATE", "knowledge_categories", category.id, user_id)
        return category

    def create_article(self, data, user_id: int | None = None):
        if data.category_id is not None:
            category = self.repo.get_category(data.category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Knowledge category not found")
            self._require_same_tenant(category, data.tenant_id)
        article = self.repo.add(KnowledgeArticle(**data.model_dump()))
        self.repo.audit("CREATE", "knowledge_articles", article.id, user_id or data.created_by)
        return article

    def update_article(self, article_id: int, data, user_id: int | None = None):
        article = self.repo.get_article(article_id)
        if not article or article.is_archived:
            raise HTTPException(status_code=404, detail="Knowledge article not found")
        values = data.model_dump(exclude_unset=True)
        if "category_id" in values and values["category_id"] is not None:
            category = self.repo.get_category(values["category_id"])
            if not category:
                raise HTTPException(status_code=404, detail="Knowledge category not found")
            self._require_same_tenant(category, article.tenant_id)
        content_changed = any(key in values for key in ("title", "content", "tags"))
        for key, value in values.items():
            setattr(article, key, value)
        if content_changed:
            article.version += 1
        article = self.repo.add(article)
        self.repo.audit("UPDATE", "knowledge_articles", article.id, user_id)
        return article

    def archive_article(self, article_id: int, user_id: int | None = None):
        article = self.repo.get_article(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Knowledge article not found")
        article.is_archived = True
        self.repo.add(article)
        self.repo.audit("ARCHIVE", "knowledge_articles", article.id, user_id)
        return {"message": "Knowledge article archived"}

    def create_form(self, data, user_id: int | None = None):
        form = self.repo.add(CustomForm(**data.model_dump()))
        self.repo.audit("CREATE", "custom_forms", form.id, user_id)
        return form

    def update_form(self, form_id: int, data, user_id: int | None = None):
        form = self.repo.get_form(form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Custom form not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(form, key, value)
        form = self.repo.add(form)
        self.repo.audit("UPDATE", "custom_forms", form.id, user_id)
        return form

    def disable_form(self, form_id: int, user_id: int | None = None):
        form = self.repo.get_form(form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Custom form not found")
        form.is_active = False
        self.repo.add(form)
        self.repo.audit("DISABLE", "custom_forms", form.id, user_id)
        return {"message": "Custom form disabled"}

    def add_form_field(self, form_id: int, data, user_id: int | None = None):
        form = self.repo.get_form(form_id)
        if not form:
            raise HTTPException(status_code=404, detail="Custom form not found")
        field = self.repo.add(CustomFormField(form_id=form_id, **data.model_dump()))
        self.repo.audit("CREATE", "custom_form_fields", field.id, user_id)
        return field

    def search(self, tenant_id: int, q: str, scope: str = "global"):
        q = q.strip()
        if len(q) < 2:
            raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
        cache_key = f"phase10d:search:{tenant_id}:{scope}:{q.lower()}"
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        results = {}
        if scope == "global":
            results["users"] = [{"id": u.id, "title": u.name, "subtitle": u.email, "type": "user"} for u in self.repo.search_users(tenant_id, q)]
            results["teams"] = [{"id": t.id, "title": t.name, "type": "team"} for t in self.repo.search_teams(tenant_id, q)]
        if scope in ("global", "projects"):
            results["projects"] = [{"id": p.id, "title": p.name, "status": p.status, "type": "project"} for p in self.repo.search_projects(tenant_id, q)]
        if scope in ("global", "tasks"):
            results["tasks"] = [{"id": t.id, "title": t.title, "status": t.status, "type": "task"} for t in self.repo.search_tasks(tenant_id, q)]
        if scope in ("global", "documents"):
            project_docs, docs = self.repo.search_documents(tenant_id, q)
            results["documents"] = (
                [{"id": d.id, "title": d.title, "type": "project_document"} for d in project_docs]
                + [{"id": d.id, "title": d.file_name, "type": "document"} for d in docs]
            )
        if scope in ("global", "messages"):
            workspace, channel = self.repo.search_messages(tenant_id, q)
            results["messages"] = (
                [{"id": m.id, "title": m.message[:120], "type": "workspace_message"} for m in workspace]
                + [{"id": m.id, "title": m.content[:120], "type": "channel_message"} for m in channel]
            )
        if scope == "global":
            meetings, notes = self.repo.search_meetings(tenant_id, q)
            results["meetings"] = (
                [{"id": m.id, "title": m.title, "type": "meeting"} for m in meetings]
                + [{"id": n.id, "title": n.content[:120], "type": "meeting_note"} for n in notes]
            )
            results["approvals"] = [{"id": a.id, "title": f"Approval #{a.id}", "status": a.status, "type": "approval"} for a in self.repo.search_approvals(tenant_id, q)]
            articles = self.repo.db.execute(self.repo.list_articles_stmt(tenant_id=tenant_id, q=q)).scalars().all()
            results["knowledge_articles"] = [{"id": a.id, "title": a.title, "type": "knowledge_article"} for a in articles]
        payload = {"tenant_id": tenant_id, "query": q, "scope": scope, "results": results}
        redis_client.setex(cache_key, 60, json.dumps(payload))
        return payload

    def analytics(self, tenant_id: int | None, area: str):
        cache_key = f"phase10d:analytics:{tenant_id}:{area}"
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        if area == "projects":
            rows = self.repo.project_analytics(tenant_id)
            data = {"total_projects": sum(count for _, count in rows), "by_status": {status or "unknown": count for status, count in rows}}
        elif area == "teams":
            rows = self.repo.team_analytics(tenant_id)
            data = {"teams": [{"team_id": team_id, "name": name, "active_members": count} for team_id, name, count in rows]}
        elif area == "tasks":
            rows = self.repo.analytics_counts(tenant_id)
            data = {"total_tasks": sum(count for _, count in rows), "by_status": {status or "unknown": count for status, count in rows}}
        elif area == "approvals":
            rows = self.repo.approval_analytics()
            data = {"total_approvals": sum(count for _, count in rows), "by_status": {status or "unknown": count for status, count in rows}}
        else:
            data = self.repo.document_analytics()
            data["total_documents"] = data["documents"] + data["project_documents"]
        payload = {"area": area, "tenant_id": tenant_id, "generated_at": datetime.utcnow().isoformat(), "data": data}
        redis_client.setex(cache_key, 120, json.dumps(payload))
        return payload

    def report(self, kind: str, tenant_id: int | None = None):
        rows = self.repo.recent_report_rows(kind, tenant_id)
        return {
            "report_type": kind,
            "tenant_id": tenant_id,
            "generated_at": datetime.utcnow(),
            "total": len(rows),
            "rows": [self._row_to_dict(row) for row in rows],
        }

    def _row_to_dict(self, row):
        return {
            key: value.isoformat() if hasattr(value, "isoformat") else value
            for key, value in row.__dict__.items()
            if not key.startswith("_")
        }
