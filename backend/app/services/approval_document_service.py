from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.approval_document import (
    ApprovalDocument
)
from app.models.approval import Approval
from app.models.user import User


def _is_admin(db: Session, user_id: int) -> bool:
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()

    return bool(user and user.role == "admin")


def _get_authorized_approval(
    db: Session,
    approval_id: int,
    tenant_id: int,
    user_id: int,
    allow_new_upload: bool = False
):
    approval_stmt = (
        select(Approval)
        .where(
            Approval.id == approval_id
        )
    )

    approval = db.execute(approval_stmt).scalar_one_or_none()

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    if _is_admin(db, user_id) or approval.current_escalation_to == user_id:
        return approval

    existing_upload_stmt = (
        select(ApprovalDocument)
        .where(
            ApprovalDocument.approval_id == approval_id,
            ApprovalDocument.tenant_id == tenant_id,
            ApprovalDocument.uploaded_by == user_id
        )
    )

    existing_upload = db.execute(existing_upload_stmt).scalar_one_or_none()

    if existing_upload:
        return approval

    if allow_new_upload:
        return approval

    raise HTTPException(
        status_code=403,
        detail="Approval document access denied"
    )


def _authorize_approval_document(
    db: Session,
    doc: ApprovalDocument,
    user_id: int
):
    approval_stmt = select(Approval).where(Approval.id == doc.approval_id)
    approval = db.execute(approval_stmt).scalar_one_or_none()

    if _is_admin(db, user_id):
        return

    if doc.uploaded_by == user_id:
        return

    if approval and approval.current_escalation_to == user_id:
        return

    raise HTTPException(
        status_code=403,
        detail="Approval document access denied"
    )


def upload_approval_document(
    db,
    tenant_id,
    approval_id,
    uploaded_by,
    file_name,
    file_path
):
    _get_authorized_approval(
        db,
        approval_id,
        tenant_id,
        uploaded_by,
        allow_new_upload=True
    )

    doc = ApprovalDocument(
        tenant_id=tenant_id,
        approval_id=approval_id,
        uploaded_by=uploaded_by,
        file_name=file_name,
        file_path=file_path
    )

    db.add(doc)

    db.commit()

    db.refresh(doc)

    return doc


def get_approval_documents(
    db: Session,
    approval_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None
):
    if tenant_id is not None and user_id is not None:
        _get_authorized_approval(
            db,
            approval_id,
            tenant_id,
            user_id,
            allow_new_upload=False
        )

    stmt = (
        select(ApprovalDocument)
        .where(
            ApprovalDocument.approval_id
            == approval_id
        )
    )

    return paginate(
        db,
        stmt
    )


def delete_approval_document(
    db: Session,
    document_id: int,
    tenant_id: int | None = None,
    user_id: int | None = None
):
    stmt = (
        select(ApprovalDocument)
        .where(
            ApprovalDocument.id
            == document_id
        )
    )

    doc = db.execute(
        stmt
    ).scalar_one_or_none()

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Approval document not found"
        )

    if tenant_id is not None and user_id is not None:
        if doc.tenant_id != tenant_id:
            raise HTTPException(
                status_code=403,
                detail="Cross tenant access denied"
            )

        _authorize_approval_document(
            db,
            doc,
            user_id
        )

    db.delete(doc)
    db.commit()

    return {
        "message":
        "Approval document deleted"
    }


def get_approval_document_for_download(
    db: Session,
    document_id: int,
    tenant_id: int,
    user_id: int
):
    stmt = (
        select(ApprovalDocument)
        .where(
            ApprovalDocument.id == document_id,
            ApprovalDocument.tenant_id == tenant_id
        )
    )

    doc = db.execute(stmt).scalar_one_or_none()

    if not doc:
        raise HTTPException(
            status_code=404,
            detail="Approval document not found"
        )

    _authorize_approval_document(
        db,
        doc,
        user_id
    )

    return doc
