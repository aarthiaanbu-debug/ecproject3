from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.kanban_service import get_kanban_board_service

router = APIRouter(
    prefix="/kanban",
    tags=["Kanban"]
)

# =========================
# DB Dependency
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# GET KANBAN BOARD
# =========================

@router.get("/")
def get_kanban_board(db: Session = Depends(get_db)):
    return get_kanban_board_service(db)