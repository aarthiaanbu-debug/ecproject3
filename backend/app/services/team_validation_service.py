from fastapi import HTTPException
from sqlalchemy import select

from app.models.phase10c import Team


def validate_team_workspace(db, team_id: int, workspace_id: int):
    team = db.execute(select(Team).where(Team.id == team_id)).scalar_one_or_none()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if team.workspace_id != workspace_id:
        raise HTTPException(status_code=403, detail="Team does not belong to workspace")
    return {"success": True, "message": "Team belongs to workspace"}


def validate_team_tenant(db, team_id: int, tenant_id: int):
    team = db.execute(select(Team).where(Team.id == team_id)).scalar_one_or_none()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if team.tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail="Team does not belong to tenant")
    return {"success": True, "message": "Team belongs to tenant"}
