from fastapi import FastAPI
from app.routers import health, transactions

app = FastAPI(
    title="Ebob API",
    description="API de pagos electrónicos Ebob",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])


@app.get("/", tags=["info"])
def root():
    return {"service": "ebob-api", "version": "0.1.0", "status": "running"}
