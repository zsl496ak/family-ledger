from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class Family(Base):
    __tablename__ = "families"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    invite_code: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="CNY")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    users = relationship("User", back_populates="family")
    accounts = relationship("Account", back_populates="family")
    categories = relationship("Category", back_populates="family")
    transactions = relationship("Transaction", back_populates="family")
    budgets = relationship("Budget", back_populates="family")
