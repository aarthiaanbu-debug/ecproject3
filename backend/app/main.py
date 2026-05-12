from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# DATABASE
from app.database import Base, engine

# =========================
# MODELS IMPORT
# =========================

import app.models.user
import app.models.task
import app.models.project
import app.models.kanban
import app.models.comment
import app.models.approval
import app.models.notification
import app.models.document
import app.models.audit_log

# =========================
# ROUTES IMPORT
# =========================

from app.routes import auth
from app.routes import user
from app.routes import task
from app.routes import kanban
from app.routes import comment
from app.routes import approval
from app.routes import analytics
from app.routes import notification
from app.routes import document
from app.routes import audit
from app.models import audit_log

# =========================
# FASTAPI INIT
# =========================

app = FastAPI(
    title="Enterprise Collaboration API",
    version="1.0.0",
    description="Task Management + Kanban + Approval Workflow System",
    openapi_tags=[
        {
            "name": "Auth",
            "description": "Authentication APIs"
        },
        {
            "name": "Users",
            "description": "User APIs"
        },
        {
            "name": "Task",
            "description": "Task CRUD APIs"
        },
        {
            "name": "Kanban",
            "description": "Kanban Board APIs"
        },
        {
            "name": "Comments",
            "description": "Task Comment APIs"
        },
        {
            "name": "Approval",
            "description": "Approval Workflow APIs"
        },
        {
            "name": "Analytics",
            "description": "Dashboard Analytics APIs"
        },
        {
            "name": "Notifications",
            "description": "Notification APIs"
        },
        {
            "name": "Documents",
            "description": "Document Upload APIs"
        }
    ]
)

# =========================
# CREATE TABLES
# =========================

Base.metadata.create_all(bind=engine)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTES REGISTER
# =========================

app.include_router(auth.router)

app.include_router(user.router)

app.include_router(task.router)

app.include_router(kanban.router)

app.include_router(comment.router)

app.include_router(approval.router)

app.include_router(analytics.router)

app.include_router(audit.router)

app.include_router(notification.router)

app.include_router(document.router)

# =========================
# ROOT API
# =========================

@app.get("/")
def root():

    return {
        "message": "🚀 Backend running successfully"
    }