from pydantic import BaseModel, EmailStr, BaseModel, constr

# cadastro
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6, max_length=72)

# login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# resposta
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True  # permite converter de SQLAlchemy para Pydantic
# Resposta ao fazer login (token JWT)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
