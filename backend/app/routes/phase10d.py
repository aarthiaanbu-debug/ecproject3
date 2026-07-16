from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.phase10d_repository import Phase10DRepository
from app.schemas.phase10d_schema import (
    CustomFormCreate,
    CustomFormFieldCreate,
    CustomFormFieldRead,
    CustomFormRead,
    CustomFormUpdate,
    KnowledgeArticleCreate,
    KnowledgeArticleRead,
    KnowledgeArticleUpdate,
    KnowledgeCategoryCreate,
    KnowledgeCategoryRead,
    NotificationRuleCreate,
    NotificationRuleRead,
    NotificationRuleUpdate,
    SavedSearchCreate,
    SavedSearchRead,
    WorkflowCreate,
    WorkflowExecutionCreate,
    WorkflowExecutionRead,
    WorkflowRead,
    WorkflowRuleCreate,
    WorkflowRuleRead,
    WorkflowUpdate,
)
from app.services.phase10d_service import Phase10DService
from app.utils.deps import get_current_user


workflows_router = APIRouter(prefix="/workflows", tags=["Workflow Automation"])
notification_rules_router = APIRouter(prefix="/notification-rules", tags=["Notification Rules"])
search_router = APIRouter(prefix="/search", tags=["Global Search"])
saved_searches_router = APIRouter(prefix="/saved-searches", tags=["Saved Searches"])
analytics10d_router = APIRouter(prefix="/analytics", tags=["Analytics"])
knowledge_router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])
forms_router = APIRouter(prefix="/forms", tags=["Custom Forms"])
reports_router = APIRouter(prefix="/reports", tags=["Reporting"])


def current_user_id(payload: dict | None) -> int | None:
    if not payload:
        return None
    return payload.get("user_id")


def require_platform_role(payload: dict):
    role = (payload or {}).get("role")
    if role not in {"admin", "manager"}:
        raise HTTPException(status_code=403, detail="Admin or manager role required")
    return payload


def service(db: Session):
    return Phase10DService(db)


@workflows_router.post("", response_model=WorkflowRead)
def create_workflow(payload: WorkflowCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).create_workflow(payload, current_user_id(user))


@workflows_router.get("", response_model=Page[WorkflowRead])
def list_workflows(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return paginate(db, Phase10DRepository(db).list_workflows_stmt(tenant_id))


@workflows_router.get("/{workflow_id}", response_model=WorkflowRead)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = Phase10DRepository(db).get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@workflows_router.put("/{workflow_id}", response_model=WorkflowRead)
def update_workflow(workflow_id: int, payload: WorkflowUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).update_workflow(workflow_id, payload, current_user_id(user))


@workflows_router.delete("/{workflow_id}")
def disable_workflow(workflow_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).disable_workflow(workflow_id, current_user_id(user))


@workflows_router.post("/{workflow_id}/rules", response_model=WorkflowRuleRead)
def add_workflow_rule(workflow_id: int, payload: WorkflowRuleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).add_workflow_rule(workflow_id, payload, current_user_id(user))


@workflows_router.get("/{workflow_id}/rules", response_model=Page[WorkflowRuleRead])
def list_workflow_rules(workflow_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10DRepository(db).list_rules_stmt(workflow_id))


@workflows_router.post("/{workflow_id}/execute", response_model=WorkflowExecutionRead)
def execute_workflow(workflow_id: int, payload: WorkflowExecutionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).execute_workflow(workflow_id, payload, current_user_id(user))


@workflows_router.get("/{workflow_id}/executions", response_model=Page[WorkflowExecutionRead])
def list_workflow_executions(workflow_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10DRepository(db).list_executions_stmt(workflow_id))


@notification_rules_router.post("", response_model=NotificationRuleRead)
def create_notification_rule(payload: NotificationRuleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).create_notification_rule(payload, current_user_id(user))


@notification_rules_router.get("", response_model=Page[NotificationRuleRead])
def list_notification_rules(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return paginate(db, Phase10DRepository(db).list_notification_rules_stmt(tenant_id))


@notification_rules_router.put("/{rule_id}", response_model=NotificationRuleRead)
def update_notification_rule(rule_id: int, payload: NotificationRuleUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).update_notification_rule(rule_id, payload, current_user_id(user))


@notification_rules_router.delete("/{rule_id}")
def disable_notification_rule(rule_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).disable_notification_rule(rule_id, current_user_id(user))


@search_router.get("/global")
def global_search(tenant_id: int = Query(gt=0), q: str = Query(min_length=2), db: Session = Depends(get_db)):
    return service(db).search(tenant_id, q, "global")


@search_router.get("/projects")
def search_projects(tenant_id: int = Query(gt=0), q: str = Query(min_length=2), db: Session = Depends(get_db)):
    return service(db).search(tenant_id, q, "projects")


@search_router.get("/tasks")
def search_tasks(tenant_id: int = Query(gt=0), q: str = Query(min_length=2), db: Session = Depends(get_db)):
    return service(db).search(tenant_id, q, "tasks")


@search_router.get("/documents")
def search_documents(tenant_id: int = Query(gt=0), q: str = Query(min_length=2), db: Session = Depends(get_db)):
    return service(db).search(tenant_id, q, "documents")


@search_router.get("/messages")
def search_messages(tenant_id: int = Query(gt=0), q: str = Query(min_length=2), db: Session = Depends(get_db)):
    return service(db).search(tenant_id, q, "messages")


@saved_searches_router.post("", response_model=SavedSearchRead)
def save_search(payload: SavedSearchCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service(db).save_search(payload, current_user_id(user))


@saved_searches_router.get("", response_model=Page[SavedSearchRead])
def list_saved_searches(tenant_id: int | None = None, user_id: int | None = None, db: Session = Depends(get_db)):
    return paginate(db, Phase10DRepository(db).list_saved_searches_stmt(tenant_id, user_id))


@saved_searches_router.delete("/{search_id}")
def delete_saved_search(search_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service(db).delete_saved_search(search_id, current_user_id(user))


@analytics10d_router.get("/projects")
def project_analytics(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return service(db).analytics(tenant_id, "projects")


@analytics10d_router.get("/teams")
def team_analytics(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return service(db).analytics(tenant_id, "teams")


@analytics10d_router.get("/tasks")
def task_analytics(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return service(db).analytics(tenant_id, "tasks")


@analytics10d_router.get("/approvals")
def approval_analytics(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return service(db).analytics(tenant_id, "approvals")


@analytics10d_router.get("/documents")
def document_analytics(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return service(db).analytics(tenant_id, "documents")


@knowledge_router.post("/categories", response_model=KnowledgeCategoryRead)
def create_category(payload: KnowledgeCategoryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).create_category(payload, current_user_id(user))


@knowledge_router.get("/categories", response_model=Page[KnowledgeCategoryRead])
def list_categories(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return paginate(db, Phase10DRepository(db).list_categories_stmt(tenant_id))


@knowledge_router.post("/articles", response_model=KnowledgeArticleRead)
def create_article(payload: KnowledgeArticleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service(db).create_article(payload, current_user_id(user))


@knowledge_router.get("/articles", response_model=Page[KnowledgeArticleRead])
def list_articles(tenant_id: int | None = None, category_id: int | None = None, q: str | None = None, db: Session = Depends(get_db)):
    return paginate(db, Phase10DRepository(db).list_articles_stmt(tenant_id, category_id, q))


@knowledge_router.get("/articles/{article_id}", response_model=KnowledgeArticleRead)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = Phase10DRepository(db).get_article(article_id)
    if not article or article.is_archived:
        raise HTTPException(status_code=404, detail="Knowledge article not found")
    return article


@knowledge_router.put("/articles/{article_id}", response_model=KnowledgeArticleRead)
def update_article(article_id: int, payload: KnowledgeArticleUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service(db).update_article(article_id, payload, current_user_id(user))


@knowledge_router.delete("/articles/{article_id}")
def archive_article(article_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service(db).archive_article(article_id, current_user_id(user))


@forms_router.post("", response_model=CustomFormRead)
def create_form(payload: CustomFormCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).create_form(payload, current_user_id(user))


@forms_router.get("", response_model=Page[CustomFormRead])
def list_forms(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return paginate(db, Phase10DRepository(db).list_forms_stmt(tenant_id))


@forms_router.get("/{form_id}", response_model=CustomFormRead)
def get_form(form_id: int, db: Session = Depends(get_db)):
    form = Phase10DRepository(db).get_form(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Custom form not found")
    return form


@forms_router.put("/{form_id}", response_model=CustomFormRead)
def update_form(form_id: int, payload: CustomFormUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).update_form(form_id, payload, current_user_id(user))


@forms_router.delete("/{form_id}")
def disable_form(form_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).disable_form(form_id, current_user_id(user))


@forms_router.post("/{form_id}/fields", response_model=CustomFormFieldRead)
def add_form_field(form_id: int, payload: CustomFormFieldCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_platform_role(user)
    return service(db).add_form_field(form_id, payload, current_user_id(user))


@forms_router.get("/{form_id}/fields", response_model=Page[CustomFormFieldRead])
def list_form_fields(form_id: int, db: Session = Depends(get_db)):
    return paginate(db, Phase10DRepository(db).list_fields_stmt(form_id))


@reports_router.get("/projects")
def project_report(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return service(db).report("projects", tenant_id)


@reports_router.get("/tasks")
def task_report(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return service(db).report("tasks", tenant_id)


@reports_router.get("/approvals")
def approval_report(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return service(db).report("approvals", tenant_id)


@reports_router.get("/documents")
def document_report(tenant_id: int | None = None, db: Session = Depends(get_db)):
    return service(db).report("documents", tenant_id)
