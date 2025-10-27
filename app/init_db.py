from app.core.database import Base, engine
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)