from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas.budget import BudgetCreate, BudgetUpdate, BudgetOut
from ..services import budget_service
from .deps import get_current_user

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("")
def list_budgets(year: int, month: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    budgets = budget_service.get_budgets(db, current_user.family_id, year, month)
    return [BudgetOut.model_validate(b) for b in budgets]


@router.post("", response_model=BudgetOut)
def create_budget(req: BudgetCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    budget = budget_service.create_budget(db, current_user.family_id, req.model_dump())
    return BudgetOut.model_validate(budget)


@router.get("/overview")
def budget_overview(year: int, month: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    budgets = budget_service.get_budgets(db, current_user.family_id, year, month)
    total_budget = sum(float(b.amount) for b in budgets)
    total_spent = sum(float(b.spent or 0) for b in budgets)
    return {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "total_remaining": total_budget - total_spent,
        "budgets": [BudgetOut.model_validate(b) for b in budgets],
    }


@router.get("/{budget_id}", response_model=BudgetOut)
def get_budget(budget_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    budget = budget_service.get_budget(db, budget_id, current_user.family_id)
    if not budget:
        raise HTTPException(status_code=404, detail="预算不存在")
    return BudgetOut.model_validate(budget)


@router.put("/{budget_id}", response_model=BudgetOut)
def update_budget(budget_id: int, req: BudgetUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    budget = budget_service.get_budget(db, budget_id, current_user.family_id)
    if not budget:
        raise HTTPException(status_code=404, detail="预算不存在")
    return budget_service.update_budget(db, budget, req.model_dump(exclude_unset=True))


@router.delete("/{budget_id}")
def delete_budget(budget_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    budget = budget_service.get_budget(db, budget_id, current_user.family_id)
    if not budget:
        raise HTTPException(status_code=404, detail="预算不存在")
    budget_service.delete_budget(db, budget)
    return {"message": "删除成功"}
