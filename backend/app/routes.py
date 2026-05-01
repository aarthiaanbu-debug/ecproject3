from fastapi import APIRouter
from app.database import SessionLocal

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Backend working"}