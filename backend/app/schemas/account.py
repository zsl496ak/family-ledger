from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class AccountCreate(BaseModel):
    name: str
    account_type: str
    icon: str | None = None
    color: str | None = None
    initial_balance: Decimal = Decimal("0")
    sort_order: int = 0


class AccountUpdate(BaseModel):
    name: str | None = None
    account_type: str | None = None
    icon: str | None = None
    color: str | None = None
    initial_balance: Decimal | None = None
    sort_order: int | None = None


class AccountOut(BaseModel):
    id: int
    family_id: int
    name: str
    account_type: str
    icon: str | None
    color: str | None
    initial_balance: Decimal
    is_active: bool
    sort_order: int
    created_at: datetime
    balance: Decimal | None = None

    model_config = {"from_attributes": True}
