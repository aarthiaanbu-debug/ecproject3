from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File

from app.database import SessionLocal
from app.models.document import Document

import shutil
import os

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# DATABASE
# =========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# =========================
# UPLOAD DOCUMENT
# =========================

@router.post("/upload")
async def upload_document(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_document = Document(
        file_name=file.filename,
        file_path=file_path,
        version="1.0",
        task_id=task_id
    )

    db.add(new_document)

    db.commit()

    db.refresh(new_document)

    return {
        "message": "File uploaded",
        "id": new_document.id
    }

# =========================
# GET DOCUMENTS
# =========================

@router.get("/")
def get_documents(
    db: Session = Depends(get_db)
):

    documents = db.query(Document).all()

    return documents