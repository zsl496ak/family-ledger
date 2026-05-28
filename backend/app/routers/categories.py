from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from ..services import category_service
from .deps import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(category_type: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.get_categories(db, current_user.family_id, category_type)


@router.post("", response_model=CategoryOut)
def create_category(req: CategoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return category_service.create_category(db, current_user.family_id, req.model_dump())


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, req: CategoryUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id, current_user.family_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return category_service.update_category(db, category, req.model_dump(exclude_unset=True))


@router.delete("/{category_id}")
def delete_category(category_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id, current_user.family_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    category_service.soft_delete_category(db, category)
    return {"message": "删除成功"}
