from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas.account import AccountCreate, AccountUpdate, AccountOut
from ..services import account_service
from .deps import get_current_user

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=list[AccountOut])
def list_accounts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    accounts = account_service.get_accounts(db, current_user.family_id)
    result = []
    for acc in accounts:
        out = AccountOut.model_validate(acc)
        out.balance = float(account_service.compute_balance(db, acc))
        result.append(out)
    return result


@router.post("", response_model=AccountOut)
def create_account(req: AccountCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = account_service.create_account(db, current_user.family_id, req.model_dump())
    out = AccountOut.model_validate(account)
    out.balance = float(account.initial_balance)
    return out


@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = account_service.get_account(db, account_id, current_user.family_id)
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")
    out = AccountOut.model_validate(account)
    out.balance = float(account_service.compute_balance(db, account))
    return out


@router.put("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, req: AccountUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = account_service.get_account(db, account_id, current_user.family_id)
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")
    account = account_service.update_account(db, account, req.model_dump(exclude_unset=True))
    out = AccountOut.model_validate(account)
    out.balance = float(account_service.compute_balance(db, account))
    return out


@router.delete("/{account_id}")
def delete_account(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = account_service.get_account(db, account_id, current_user.family_id)
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")
    account_service.soft_delete_account(db, account)
    return {"message": "删除成功"}
