from pydantic import BaseModel


class RolePermissionCreate(BaseModel):

    role_name: str
    module_name: str

    can_create: bool = False
    can_read: bool = True
    can_update: bool = False
    can_delete: bool = False


class RolePermissionUpdate(BaseModel):

    can_create: bool
    can_read: bool
    can_update: bool
    can_delete: bool


class RolePermissionResponse(BaseModel):

    id: int
    role_name: str
    module_name: str

    can_create: bool
    can_read: bool
    can_update: bool
    can_delete: bool

    model_config = {
        "from_attributes": True
    }