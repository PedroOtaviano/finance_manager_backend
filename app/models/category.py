from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    type = Column(String(10), nullable=False)  # 'income' ou 'expense'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("type IN ('income','expense')", name="check_category_type"),
    )

    # Relacionamentos
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")