from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import Account, Transaction


def get_accounts(db: Session, family_id: int) -> list[Account]:
    return db.query(Account).filter(Account.family_id == family_id, Account.is_active == True).order_by(Account.sort_order).all()


def get_account(db: Session, account_id: int, family_id: int) -> Account | None:
    return db.query(Account).filter(Account.id == account_id, Account.family_id == family_id).first()


def compute_balance(db: Session, account: Account) -> Decimal:
    income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.account_id == account.id,
        Transaction.transaction_type == "income",
        Transaction.family_id == account.family_id,
    ).scalar()

    expense = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.account_id == account.id,
        Transaction.transaction_type == "expense",
        Transaction.family_id == account.family_id,
    ).scalar()

    transfer_out = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.account_id == account.id,
        Transaction.transaction_type == "transfer",
        Transaction.family_id == account.family_id,
    ).scalar()

    transfer_in = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.transfer_to_account_id == account.id,
        Transaction.transaction_type == "transfer",
        Transaction.family_id == account.family_id,
    ).scalar()

    return account.initial_balance + income - expense - transfer_out + transfer_in


def create_account(db: Session, family_id: int, data: dict) -> Account:
    account = Account(family_id=family_id, **data)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def update_account(db: Session, account: Account, data: dict) -> Account:
    for key, value in data.items():
        if value is not None:
            setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account


def soft_delete_account(db: Session, account: Account):
    account.is_active = False
    db.commit()
