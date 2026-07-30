from fastapi import FastAPI
from app.api.health import router as healther_router

app = FastAPI(
    title="ContractClarify AI API",
    description="Backend API for full-stack AI document assistant",
    version="0.1.0",
)

app.include_router(healther_router)

@app.get("/")
def root():
    return {
        "message": "ContractClarify AI API is runnning"
    }