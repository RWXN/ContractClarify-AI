from fastapi import FastAPI
from app.api.health import router as healthe_router
from app.api.auth import router as auth_router

app = FastAPI(
    title="ContractClarify AI API",
    description="Backend API for full-stack AI document assistant",
    version="0.1.0",
)

app.include_router(healthe_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "ContractClarify AI API is runnning"
    }