from datetime import datetime
from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    family_id: int
    username: str
    email: str
    role: str
    avatar: str | None = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    username: str | None = None
    avatar: str | None = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
