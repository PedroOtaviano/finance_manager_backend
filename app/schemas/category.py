from pydantic import BaseModel
from typing import Optional
from enum import Enum

class CategoryType(str, Enum):
    income = "income"
    expense = "expense"

# Criar categoria
class CategoryCreate(BaseModel):
    name: str
    type: CategoryType

# Atualizar categoria
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None

# Retorno da API
class CategoryOut(BaseModel):
    id: int
    name: str
    type: CategoryType

    class Config:
        from_attributes = True

