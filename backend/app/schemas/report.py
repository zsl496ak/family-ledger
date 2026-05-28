from decimal import Decimal
from pydantic import BaseModel


class MonthlySummary(BaseModel):
    year: int
    month: int
    total_income: Decimal
    total_expense: Decimal
    net_amount: Decimal
    transaction_count: int


class CategoryBreakdown(BaseModel):
    category_id: int
    category_name: str
    category_type: str
    amount: Decimal
    percentage: float
    icon: str | None
    color: str | None


class TrendData(BaseModel):
    month: str
    income: Decimal
    expense: Decimal


class AccountBalance(BaseModel):
    account_id: int
    account_name: str
    account_type: str
    balance: Decimal
    icon: str | None
    color: str | None
