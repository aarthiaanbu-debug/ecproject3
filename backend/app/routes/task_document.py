from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)
from fastapi.responses import FileResponse
import os
UPLOAD_DIR = "uploads/task_documents"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.database import get_db

from app.schemas.task_document_schema import (
    TaskDocumentResponse
)

from app.services.task_document_service import (
    upload_task_document,
    get_task_document_for_download,
    get_task_documents,
    delete_task_document
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt"
}


def validate_upload_file(file: UploadFile) -> str:
    file_name = os.path.basename(file.filename or "")
    extension = os.path.splitext(file_name)[1].lower()

    if not file_name or extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported or unsafe file type"
        )

    return file_name

router = APIRouter(
    prefix="/task-documents",
    tags=["Task Documents"]
)
@router.post(
    "/upload"
)
async def upload_document(
    tenant_id: int = Form(...),
    task_id: int = Form(...),
    uploaded_by: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_name = validate_upload_file(file)

    file_path = (
        f"{UPLOAD_DIR}/{file_name}"
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    return upload_task_document(
        db,
        tenant_id,
        task_id,
        uploaded_by,
        file_name,
        file_path
    )


@router.get(
    "/task/{task_id}",
    response_model=Page[
        TaskDocumentResponse
    ]
)
def list_documents(
    task_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_task_documents(
        db,
        task_id,
        tenant_id,
        user_id
    )


@router.delete(
    "/{document_id}"
)
def delete_document(
    document_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db)
):
    return delete_task_document(
        db,
        document_id,
        tenant_id,
        user_id
    )


@router.get(
    "/{document_id}/download"
)
def download_document(
    document_id: int,
    tenant_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    doc = get_task_document_for_download(
        db,
        document_id,
        tenant_id,
        user_id
    )

    if not os.path.exists(doc.file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        doc.file_path,
        filename=doc.file_name
    )
