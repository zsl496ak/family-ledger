from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel


class TransactionCreate(BaseModel):
    account_id: int
    category_id: int | None = None
    transaction_type: str
    amount: Decimal
    note: str | None = None
    transaction_date: date
    transfer_to_account_id: int | None = None


class TransactionUpdate(BaseModel):
    account_id: int | None = None
    category_id: int | None = None
    transaction_type: str | None = None
    amount: Decimal | None = None
    note: str | None = None
    transaction_date: date | None = None
    transfer_to_account_id: int | None = None


class TransactionOut(BaseModel):
    id: int
    family_id: int
    account_id: int
    category_id: int | None
    transaction_type: str
    amount: float
    note: str | None
    transaction_date: date
    creator_id: int
    transfer_to_account_id: int | None
    created_at: datetime
    updated_at: datetime
    creator_name: str | None = None
    category_name: str | None = None
    account_name: str | None = None
    transfer_to_account_name: str | None = None

    model_config = {"from_attributes": True}


class TransactionFilter(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    transaction_type: str | None = None
    category_id: int | None = None
    account_id: int | None = None
    search: str | None = None
    page: int = 1
    page_size: int = 20


class TransactionSummary(BaseModel):
    total_income: float
    total_expense: float
    net_amount: float
    count: int
