from pydantic import BaseModel


class MonthlySummary(BaseModel):
    year: int
    month: int
    total_income: float
    total_expense: float
    net_amount: float
    transaction_count: int


class CategoryBreakdown(BaseModel):
    category_id: int
    category_name: str
    category_type: str
    amount: float
    percentage: float
    icon: str | None
    color: str | None


class TrendData(BaseModel):
    month: str
    income: float
    expense: float


class AccountBalance(BaseModel):
    account_id: int
    account_name: str
    account_type: str
    balance: float
    icon: str | None
    color: str | None
