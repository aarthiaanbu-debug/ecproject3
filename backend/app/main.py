from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# DB
from app.database import Base, engine

# 🔥 IMPORTANT: MODELS IMPORT FIRST (MUST)
from app.models import user, task, project, kanban

# ROUTES IMPORT
from app.routes import (
    task,
    comment,
    approval,
    analytics,
    user,
    auth,
    kanban
)

# APP INIT
app = FastAPI(
    title="Enterprise Collaboration API",
    version="1.0.0",
    description="Task Management + Kanban + Approval System API",
    openapi_tags=[
        {"name": "Auth", "description": "Authentication APIs"},
        {"name": "Task", "description": "Task CRUD operations"},
        {"name": "Kanban", "description": "Kanban board APIs"},
        {"name": "Comments", "description": "Task comments"},
        {"name": "Approval", "description": "Approval workflow"},
        {"name": "Analytics", "description": "Dashboard analytics"},
        {"name": "Users", "description": "User management"},
    ]
)

# 🔥 CREATE TABLES AFTER MODELS LOAD
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES REGISTER
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(kanban.router)
app.include_router(comment.router)
app.include_router(approval.router)
app.include_router(analytics.router)

# ROOT
@app.get("/")
def root():
    return {"message": "🚀 Backend running successfully"}