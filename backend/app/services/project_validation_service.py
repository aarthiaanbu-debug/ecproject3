from fastapi import HTTPException
from sqlalchemy import select

from app.models.phase10c import Project


def validate_project_workspace(db, project_id: int, workspace_id: int):
    project = db.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.workspace_id != workspace_id:
        raise HTTPException(status_code=403, detail="Project does not belong to workspace")
    return {"success": True, "message": "Project belongs to workspace"}


def validate_project_tenant(db, project_id: int, tenant_id: int):
    project = db.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail="Project does not belong to tenant")
    return {"success": True, "message": "Project belongs to tenant"}
