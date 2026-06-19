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
UPLOAD_DIR = "uploads/approval_documents"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

from sqlalchemy.orm import Session

from fastapi_pagination import Page

from app.database import get_db

from app.schemas.approval_document_schema import (
    ApprovalDocumentResponse
)

from app.services.approval_document_service import (
    upload_approval_document,
    get_approval_document_for_download,
    get_approval_documents,
    delete_approval_document
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
    prefix="/approval-documents",
    tags=["Approval Documents"]
)
@router.post(
    "/upload"
)
async def upload_document(
    tenant_id: int = Form(...),
    approval_id: int = Form(...),
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

    return upload_approval_document(
        db,
        tenant_id,
        approval_id,
        uploaded_by,
        file_name,
        file_path
    )


@router.get(
    "/approval/{approval_id}",
    response_model=Page[
        ApprovalDocumentResponse
    ]
)
def list_documents(
    approval_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_approval_documents(
        db,
        approval_id,
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
    return delete_approval_document(
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
    doc = get_approval_document_for_download(
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
