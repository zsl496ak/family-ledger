from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import Transaction, Account
from ..schemas.transaction import TransactionFilter, TransactionSummary


def get_transactions(db: Session, family_id: int, filters: TransactionFilter) -> tuple[list[Transaction], int]:
    query = db.query(Transaction).filter(Transaction.family_id == family_id)

    if filters.date_from:
        query = query.filter(Transaction.transaction_date >= filters.date_from)
    if filters.date_to:
        query = query.filter(Transaction.transaction_date <= filters.date_to)
    if filters.transaction_type:
        query = query.filter(Transaction.transaction_type == filters.transaction_type)
    if filters.category_id:
        query = query.filter(Transaction.category_id == filters.category_id)
    if filters.account_id:
        query = query.filter(Transaction.account_id == filters.account_id)
    if filters.search:
        query = query.filter(Transaction.note.ilike(f"%{filters.search}%"))

    total = query.count()
    items = query.order_by(Transaction.transaction_date.desc(), Transaction.created_at.desc()).offset(
        (filters.page - 1) * filters.page_size
    ).limit(filters.page_size).all()

    # Enrich with names
    for item in items:
        item.creator_name = item.creator.username if item.creator else None
        item.category_name = item.category.name if item.category else None
        account = db.query(Account).filter(Account.id == item.account_id).first()
        item.account_name = account.name if account else None
        if item.transfer_to_account_id:
            to_account = db.query(Account).filter(Account.id == item.transfer_to_account_id).first()
            item.transfer_to_account_name = to_account.name if to_account else None

    return items, total


def get_transaction(db: Session, transaction_id: int, family_id: int) -> Transaction | None:
    return db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.family_id == family_id).first()


def create_transaction(db: Session, family_id: int, creator_id: int, data: dict) -> Transaction:
    transaction = Transaction(family_id=family_id, creator_id=creator_id, **data)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def update_transaction(db: Session, transaction: Transaction, data: dict) -> Transaction:
    for key, value in data.items():
        if value is not None:
            setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction: Transaction):
    db.delete(transaction)
    db.commit()


def get_summary(db: Session, family_id: int, date_from=None, date_to=None) -> TransactionSummary:
    query = db.query(Transaction).filter(Transaction.family_id == family_id)
    if date_from:
        query = query.filter(Transaction.transaction_date >= date_from)
    if date_to:
        query = query.filter(Transaction.transaction_date <= date_to)

    total_income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.family_id == family_id,
        Transaction.transaction_type == "income",
        *([Transaction.transaction_date >= date_from] if date_from else []),
        *([Transaction.transaction_date <= date_to] if date_to else []),
    ).scalar()

    total_expense = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.family_id == family_id,
        Transaction.transaction_type == "expense",
        *([Transaction.transaction_date >= date_from] if date_from else []),
        *([Transaction.transaction_date <= date_to] if date_to else []),
    ).scalar()

    count = query.count()

    return TransactionSummary(
        total_income=total_income,
        total_expense=total_expense,
        net_amount=total_income - total_expense,
        count=count,
    )
