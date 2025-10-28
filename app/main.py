from fastapi import FastAPI
from app.routes import auth, transactions, dashboard, categories
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Finance Manager API",
    description="API para gerenciar usuários, categorias e transações financeiras.",
    version="1.0.0",
    contact={
        "name": "Pedro",
        "email": "pedro.redes23@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/health")
def health():
    return {"status": "ok"}