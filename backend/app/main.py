from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# DB
from app.database import Base, engine

# 🔥 IMPORTANT: LOAD MODELS FIRST
from app.models import user, task, project, kanban

# ✅ CORRECT IMPORTS (NO backend.app)
from app.routes import auth, task, kanban, approval, analytics, user, comment

# APP INIT
app = FastAPI(
    title="Enterprise Collaboration API",
    version="1.0.0"
)

# CREATE TABLES
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES REGISTER
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