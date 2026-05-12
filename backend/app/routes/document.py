from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.services import document_service

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/upload")
def upload_file(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    return document_service.upload_document(
        db,
        task_id,
        file
    )


@router.get("/")
def get_documents(
    db: Session = Depends(get_db)
):

    return document_service.get_documents(db)