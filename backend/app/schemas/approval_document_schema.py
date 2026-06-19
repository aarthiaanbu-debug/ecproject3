from pydantic import BaseModel


class ApprovalDocumentResponse(BaseModel):
    id: int
    file_name: str

    model_config = {
        "from_attributes": True
    }