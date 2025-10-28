from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal
from enum import Enum

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

# Criar transação
class TransactionCreate(BaseModel):
    category_id: int
    type: TransactionType
    amount: Decimal
    date: date
    note: Optional[str] = None

# Atualizar transação
class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    type: Optional[TransactionType] = None
    amount: Optional[Decimal] = None
    date: Optional[date] = None
    note: Optional[str] = None

# Retorno da API
class TransactionOut(BaseModel):
    id: int
    category_id: int
    type: TransactionType
    amount: Decimal
    date: date
    note: Optional[str]

    class Config:
        from_attributes = True
