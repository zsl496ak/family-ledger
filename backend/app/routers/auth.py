from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas.auth import LoginRequest, RegisterRequest, RegisterJoinRequest, TokenResponse, RefreshRequest
from ..schemas.user import UserOut, UserUpdate, PasswordChange
from ..services import auth_service
from .deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    user = auth_service.register(db, req.username, req.email, req.password, req.family_name)
    token_data = {"sub": user.id, "family_id": user.family_id, "role": user.role}
    return TokenResponse(
        access_token=auth_service.create_access_token(token_data),
        refresh_token=auth_service.create_refresh_token(token_data),
    )


@router.post("/register/join", response_model=TokenResponse)
def register_join(req: RegisterJoinRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    try:
        user = auth_service.register_join(db, req.username, req.email, req.password, req.invite_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token_data = {"sub": user.id, "family_id": user.family_id, "role": user.role}
    return TokenResponse(
        access_token=auth_service.create_access_token(token_data),
        refresh_token=auth_service.create_refresh_token(token_data),
    )


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate(db, req.email, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    token_data = {"sub": user.id, "family_id": user.family_id, "role": user.role}
    return TokenResponse(
        access_token=auth_service.create_access_token(token_data),
        refresh_token=auth_service.create_refresh_token(token_data),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(req: RefreshRequest, db: Session = Depends(get_db)):
    payload = auth_service.decode_token(req.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="无效的刷新令牌")
    user = auth_service.get_user_by_id(db, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    token_data = {"sub": user.id, "family_id": user.family_id, "role": user.role}
    return TokenResponse(
        access_token=auth_service.create_access_token(token_data),
        refresh_token=auth_service.create_refresh_token(token_data),
    )


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
def update_me(req: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if req.username is not None:
        current_user.username = req.username
    if req.avatar is not None:
        current_user.avatar = req.avatar
    db.commit()
    db.refresh(current_user)
    return current_user


@router.put("/password")
def change_password(req: PasswordChange, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not auth_service.verify_password(req.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="原密码错误")
    current_user.hashed_password = auth_service.hash_password(req.new_password)
    db.commit()
    return {"message": "密码修改成功"}
