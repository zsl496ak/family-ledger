from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Transaction, Account, Category
from ..services import account_service
from .deps import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly")
def monthly_report(year: int, month: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    date_from = date(year, month, 1)
    if month == 12:
        date_to = date(year + 1, 1, 1)
    else:
        date_to = date(year, month + 1, 1)

    income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.family_id == current_user.family_id,
        Transaction.transaction_type == "income",
        Transaction.transaction_date >= date_from,
        Transaction.transaction_date < date_to,
    ).scalar()

    expense = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.family_id == current_user.family_id,
        Transaction.transaction_type == "expense",
        Transaction.transaction_date >= date_from,
        Transaction.transaction_date < date_to,
    ).scalar()

    count = db.query(Transaction).filter(
        Transaction.family_id == current_user.family_id,
        Transaction.transaction_date >= date_from,
        Transaction.transaction_date < date_to,
    ).count()

    return {
        "year": year, "month": month,
        "total_income": float(income), "total_expense": float(expense),
        "net_amount": float(income) - float(expense), "transaction_count": count,
    }


@router.get("/yearly")
def yearly_report(year: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    months = []
    for m in range(1, 13):
        date_from = date(year, m, 1)
        if m == 12:
            date_to = date(year + 1, 1, 1)
        else:
            date_to = date(year, m + 1, 1)

        income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.family_id == current_user.family_id,
            Transaction.transaction_type == "income",
            Transaction.transaction_date >= date_from,
            Transaction.transaction_date < date_to,
        ).scalar()

        expense = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.family_id == current_user.family_id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= date_from,
            Transaction.transaction_date < date_to,
        ).scalar()

        months.append({
            "month": m, "income": float(income), "expense": float(expense),
            "net": float(income) - float(expense),
        })

    total_income = sum(m["income"] for m in months)
    total_expense = sum(m["expense"] for m in months)
    return {
        "year": year, "months": months,
        "total_income": total_income, "total_expense": total_expense,
        "net_amount": total_income - total_expense,
    }


@router.get("/category-breakdown")
def category_breakdown(year: int, month: int, transaction_type: str = "expense", current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    date_from = date(year, month, 1)
    if month == 12:
        date_to = date(year + 1, 1, 1)
    else:
        date_to = date(year, month + 1, 1)

    rows = db.query(
        Transaction.category_id,
        func.sum(Transaction.amount).label("total"),
    ).filter(
        Transaction.family_id == current_user.family_id,
        Transaction.transaction_type == transaction_type,
        Transaction.transaction_date >= date_from,
        Transaction.transaction_date < date_to,
        Transaction.category_id.isnot(None),
    ).group_by(Transaction.category_id).all()

    grand_total = sum(float(r.total) for r in rows) or 1

    result = []
    for row in rows:
        cat = db.query(Category).filter(Category.id == row.category_id).first()
        if cat:
            result.append({
                "category_id": cat.id, "category_name": cat.name,
                "category_type": cat.category_type,
                "amount": float(row.total), "percentage": float(row.total) / grand_total * 100,
                "icon": cat.icon, "color": cat.color,
            })

    return result


@router.get("/trend")
def trend(year: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    months = []
    for m in range(1, 13):
        date_from = date(year, m, 1)
        if m == 12:
            date_to = date(year + 1, 1, 1)
        else:
            date_to = date(year, m + 1, 1)

        income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.family_id == current_user.family_id,
            Transaction.transaction_type == "income",
            Transaction.transaction_date >= date_from,
            Transaction.transaction_date < date_to,
        ).scalar()

        expense = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.family_id == current_user.family_id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= date_from,
            Transaction.transaction_date < date_to,
        ).scalar()

        months.append({"month": f"{m}月", "income": float(income), "expense": float(expense)})

    return months


@router.get("/account-balances")
def account_balances(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    accounts = account_service.get_accounts(db, current_user.family_id)
    result = []
    for acc in accounts:
        balance = account_service.compute_balance(db, acc)
        result.append({
            "account_id": acc.id, "account_name": acc.name,
            "account_type": acc.account_type, "balance": float(balance),
            "icon": acc.icon, "color": acc.color,
        })
    return result
