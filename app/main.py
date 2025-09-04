from fastapi import FastAPI
from .routers import search, financials

app = FastAPI(title="FastAPI + OpenSearch Example")

app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(financials.router, prefix="/financials", tags=["Financials"])

@app.get("/")
def root():
    return {"message": "FastAPI + OpenSearch running!"}
