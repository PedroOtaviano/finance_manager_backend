from pydantic import BaseModel
from typing import Optional

# Criar categoria
class CategoryCreate(BaseModel):
    name: str
    type: str  # 'income' ou 'expense'

# Atualizar categoria
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None

# Retorno da API
class CategoryOut(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        orm_mode = True
