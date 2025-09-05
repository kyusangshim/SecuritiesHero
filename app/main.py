from fastapi import FastAPI
from .routers import search, financials
from app.AI.routers.equity_router import router as equity_router

app = FastAPI(title="FastAPI + OpenSearch Example")

app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(financials.router, prefix="/financials", tags=["Financials"])
app.include_router(equity_router)

@app.get("/")
def root():
    return {"message": "FastAPI + OpenSearch running!"}
