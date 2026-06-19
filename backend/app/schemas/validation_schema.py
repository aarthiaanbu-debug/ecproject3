from pydantic import BaseModel


class ValidationResponse(BaseModel):
    success: bool
    message: str