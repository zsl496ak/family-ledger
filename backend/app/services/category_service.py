from sqlalchemy.orm import Session

from ..models import Category


def get_categories(db: Session, family_id: int, category_type: str | None = None) -> list[Category]:
    query = db.query(Category).filter(Category.family_id == family_id, Category.is_active == True)
    if category_type:
        query = query.filter(Category.category_type == category_type)
    return query.order_by(Category.sort_order).all()


def get_category(db: Session, category_id: int, family_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id, Category.family_id == family_id).first()


def create_category(db: Session, family_id: int, data: dict) -> Category:
    category = Category(family_id=family_id, **data)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category: Category, data: dict) -> Category:
    for key, value in data.items():
        if value is not None:
            setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def soft_delete_category(db: Session, category: Category):
    category.is_active = False
    db.commit()
