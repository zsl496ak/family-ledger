from decimal import Decimal
from pydantic import BaseModel


class BudgetCreate(BaseModel):
    category_id: int
    year: int
    month: int
    amount: Decimal


class BudgetUpdate(BaseModel):
    amount: Decimal | None = None


class BudgetOut(BaseModel):
    id: int
    family_id: int
    category_id: int
    year: int
    month: int
    amount: float
    spent: float | None = None
    remaining: float | None = None
    percentage: float | None = None
    category_name: str | None = None

    model_config = {"from_attributes": True}
