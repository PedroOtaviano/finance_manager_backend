from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, func, CheckConstraint, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    type = Column(String(10), nullable=False)  # 'income' ou 'expense'
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("type IN ('income','expense')", name="check_transaction_type"),
    )

    # Relacionamentos
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")