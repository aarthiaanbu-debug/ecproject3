from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# DATABASE
from app.database import Base, engine
from app.db_migrations import add_missing_columns

# RATE LIMIT
from slowapi.middleware import SlowAPIMiddleware
from app.middleware.rate_limit import limiter

# =========================
# MODELS IMPORT
# =========================

import app.models.user
import app.models.task
import app.models.kanban
import app.models.comment
import app.models.approval
import app.models.notification
import app.models.document
import app.models.audit
import app.models.sla
import app.models.workflow
import app.models.leave
import app.models.workspace
import app.models.workspace_member
import app.models.channel
import app.models.channel_member


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
from app.routes import websocket
from app.routes import payment
from app.routes import stripe
from app.routes import stripe_webhook
from app.routes import sla
from app.routes import workflow
from app.routes import tenant
from app.routes import leave
from app.routes import workspace
from app.routes import channel

# =========================
# FASTAPI INIT
# =========================

app = FastAPI(
    title="Enterprise Collaboration API",
    version="1.0.0",
    description="Task Management + Kanban + Approval Workflow System",
)

# =========================
# CREATE TABLES
# =========================

Base.metadata.create_all(bind=engine)
add_missing_columns()

# =========================
# CORS
# =========================

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# RATE LIMIT
# =========================

app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
)

# =========================
# ROUTERS
# =========================

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(kanban.router)
app.include_router(comment.router)
app.include_router(approval.router)
app.include_router(analytics.router)
app.include_router(analytics.dashboard_router)
app.include_router(notification.router)
app.include_router(document.router)
app.include_router(audit.router)
app.include_router(websocket.router)
app.include_router(payment.router)
app.include_router(stripe.router)
app.include_router(stripe_webhook.router)
app.include_router(sla.router)
app.include_router(workflow.router)
app.include_router(tenant.router)
app.include_router(leave.router)
app.include_router(workspace.router)
app.include_router(channel.router)

# =========================
# ROOT
# =========================

@app.get("/")
def root():

    return {
        "message": "🚀 Backend running successfully"
    }
