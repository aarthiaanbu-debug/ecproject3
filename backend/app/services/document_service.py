import os
import shutil

from sqlalchemy import select

from app.models.document import Document

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def upload_document(
    db,
    task_id,
    file
):

    file_path = (
        f"{UPLOAD_FOLDER}/{file.filename}"
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    document = Document(
        file_name=file.filename,
        file_path=file_path,
        task_id=task_id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message": "File uploaded",
        "id": document.id
    }


def get_documents(db):

    stmt = select(Document)

    return db.execute(stmt).scalars().all()
