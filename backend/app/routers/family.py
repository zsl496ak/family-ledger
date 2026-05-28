from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..models import User, Family
from ..services import auth_service
from .deps import get_current_user

router = APIRouter(prefix="/family", tags=["family"])


class FamilyUpdate(BaseModel):
    name: str | None = None


class RoleUpdate(BaseModel):
    role: str


@router.get("")
def get_family(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    family = db.query(Family).filter(Family.id == current_user.family_id).first()
    return {
        "id": family.id, "name": family.name, "invite_code": family.invite_code,
        "currency": family.currency, "created_at": family.created_at,
    }


@router.put("")
def update_family(req: FamilyUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    family = db.query(Family).filter(Family.id == current_user.family_id).first()
    if req.name:
        family.name = req.name
    db.commit()
    return {"message": "更新成功"}


@router.post("/regenerate-invite")
def regenerate_invite(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    family = db.query(Family).filter(Family.id == current_user.family_id).first()
    family.invite_code = auth_service.generate_invite_code()
    db.commit()
    return {"invite_code": family.invite_code}


@router.get("/members")
def list_members(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).filter(User.family_id == current_user.family_id, User.is_active == True).all()
    return [{
        "id": u.id, "username": u.username, "email": u.email,
        "role": u.role, "avatar": u.avatar, "created_at": u.created_at,
    } for u in users]


@router.put("/members/{user_id}/role")
def update_role(user_id: int, req: RoleUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    user = db.query(User).filter(User.id == user_id, User.family_id == current_user.family_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if req.role not in ("admin", "member"):
        raise HTTPException(status_code=400, detail="无效的角色")
    user.role = req.role
    db.commit()
    return {"message": "角色更新成功"}


@router.delete("/members/{user_id}")
def remove_member(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能移除自己")
    user = db.query(User).filter(User.id == user_id, User.family_id == current_user.family_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.is_active = False
    db.commit()
    return {"message": "成员已移除"}
