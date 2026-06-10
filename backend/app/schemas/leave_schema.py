from pydantic import BaseModel


class LeaveRequestCreate(BaseModel):
    employee_name: str
    reason: str
    from_date: str
    to_date: str
    requested_by: int | None = 1
