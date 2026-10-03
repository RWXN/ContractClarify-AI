from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.documents import router as documents_router

from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="ContractClarify AI API",
    description="Backend API for full-stack AI document assistant",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(documents_router)

@app.get("/")
def root():
    return {
        "message": "ContractClarify AI API is runnning"
    }