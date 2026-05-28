from datetime import datetime
from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    category_type: str
    icon: str | None = None
    color: str | None = None
    parent_id: int | None = None
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    color: str | None = None
    parent_id: int | None = None
    sort_order: int | None = None


class CategoryOut(BaseModel):
    id: int
    family_id: int
    name: str
    category_type: str
    icon: str | None
    color: str | None
    parent_id: int | None
    is_active: bool
    sort_order: int
    created_at: datetime

    model_config = {"from_attributes": True}
