from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# DATABASE
from app.database import Base, engine

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
from app.routes import stripe_webhook
from fastapi import FastAPI
from app.routes.payment import router as payment_router

app = FastAPI()

app.include_router(payment_router)

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
app.include_router(notification.router)
app.include_router(document.router)
app.include_router(audit.router)
app.include_router(websocket.router)
app.include_router(payment.router)
app.include_router(stripe_webhook.router)

# =========================
# ROOT
# =========================

@app.get("/")
def root():

    return {
        "message": "🚀 Backend running successfully"
    }