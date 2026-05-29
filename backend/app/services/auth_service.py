import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..config import settings
from ..models import Family, User
from ..models.category import Category

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain[:72], hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_sub": False})
        return payload
    except JWTError:
        return None


def generate_invite_code() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


DEFAULT_EXPENSE_CATEGORIES = [
    {"name": "餐饮", "icon": "Bowl", "color": "#F56C6C"},
    {"name": "交通", "icon": "Van", "color": "#E6A23C"},
    {"name": "购物", "icon": "ShoppingBag", "color": "#409EFF"},
    {"name": "娱乐", "icon": "Film", "color": "#67C23A"},
    {"name": "居住", "icon": "House", "color": "#909399"},
    {"name": "医疗", "icon": "FirstAidKit", "color": "#F56C6C"},
    {"name": "教育", "icon": "Reading", "color": "#409EFF"},
    {"name": "通讯", "icon": "Iphone", "color": "#E6A23C"},
    {"name": "其他支出", "icon": "More", "color": "#909399"},
]

DEFAULT_INCOME_CATEGORIES = [
    {"name": "工资", "icon": "Money", "color": "#67C23A"},
    {"name": "奖金", "icon": "Trophy", "color": "#E6A23C"},
    {"name": "投资", "icon": "TrendCharts", "color": "#409EFF"},
    {"name": "兼职", "icon": "Briefcase", "color": "#909399"},
    {"name": "红包", "icon": "Present", "color": "#F56C6C"},
    {"name": "退款", "icon": "RefreshLeft", "color": "#E6A23C"},
    {"name": "其他收入", "icon": "More", "color": "#909399"},
]


def create_default_categories(db: Session, family_id: int):
    for i, cat in enumerate(DEFAULT_EXPENSE_CATEGORIES):
        db.add(Category(
            family_id=family_id, name=cat["name"], category_type="expense",
            icon=cat["icon"], color=cat["color"], sort_order=i,
        ))
    for i, cat in enumerate(DEFAULT_INCOME_CATEGORIES):
        db.add(Category(
            family_id=family_id, name=cat["name"], category_type="income",
            icon=cat["icon"], color=cat["color"], sort_order=i,
        ))
    db.flush()


def register(db: Session, username: str, email: str, password: str, family_name: str) -> User:
    invite_code = generate_invite_code()
    family = Family(name=family_name, invite_code=invite_code)
    db.add(family)
    db.flush()

    create_default_categories(db, family.id)

    user = User(
        family_id=family.id, username=username, email=email,
        hashed_password=hash_password(password), role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def register_join(db: Session, username: str, email: str, password: str, invite_code: str) -> User:
    family = db.query(Family).filter(Family.invite_code == invite_code).first()
    if not family:
        raise ValueError("邀请码无效")

    user = User(
        family_id=family.id, username=username, email=email,
        hashed_password=hash_password(password), role="member",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()
