from pydantic import BaseModel


class TaskDocumentResponse(BaseModel):

    id: int
    file_name: str
    file_path: str

    model_config = {
        "from_attributes": True
    }