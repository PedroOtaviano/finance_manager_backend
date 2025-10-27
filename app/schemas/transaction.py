from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

# Criar transação
class TransactionCreate(BaseModel):
    category_id: int
    type: str  # 'income' ou 'expense'
    amount: Decimal
    date: date
    note: Optional[str] = None

# Atualizar transação
class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    type: Optional[str] = None
    amount: Optional[Decimal] = None
    date: Optional[date] = None
    note: Optional[str] = None

# Retorno da API
class TransactionOut(BaseModel):
    id: int
    category_id: int
    type: str
    amount: Decimal
    date: date
    note: Optional[str]

    class Config:
        orm_mode = True