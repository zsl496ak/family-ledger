from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import Budget, Transaction


def get_budgets(db: Session, family_id: int, year: int, month: int) -> list[Budget]:
    budgets = db.query(Budget).filter(
        Budget.family_id == family_id,
        Budget.year == year,
        Budget.month == month,
    ).all()

    for budget in budgets:
        spent = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.family_id == family_id,
            Transaction.category_id == budget.category_id,
            Transaction.transaction_type == "expense",
            func.strftime("%Y", Transaction.transaction_date) == str(year),
            func.strftime("%m", Transaction.transaction_date) == f"{month:02d}",
        ).scalar()

        budget.spent = spent
        budget.remaining = budget.amount - spent
        budget.percentage = float(spent / budget.amount * 100) if budget.amount > 0 else 0
        budget.category_name = budget.category.name if budget.category else None

    return budgets


def get_budget(db: Session, budget_id: int, family_id: int) -> Budget | None:
    return db.query(Budget).filter(Budget.id == budget_id, Budget.family_id == family_id).first()


def create_budget(db: Session, family_id: int, data: dict) -> Budget:
    existing = db.query(Budget).filter(
        Budget.family_id == family_id,
        Budget.category_id == data["category_id"],
        Budget.year == data["year"],
        Budget.month == data["month"],
    ).first()
    if existing:
        existing.amount = data["amount"]
        db.commit()
        db.refresh(existing)
        return existing

    budget = Budget(family_id=family_id, **data)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def update_budget(db: Session, budget: Budget, data: dict) -> Budget:
    for key, value in data.items():
        if value is not None:
            setattr(budget, key, value)
    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, budget: Budget):
    db.delete(budget)
    db.commit()
