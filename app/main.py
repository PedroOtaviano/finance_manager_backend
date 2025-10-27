from fastapi import FastAPI
from app.routes import auth, transactions, dashboard, categories

app = FastAPI(title="Finance Manager API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/health")
def health():
    return {"status": "ok"}