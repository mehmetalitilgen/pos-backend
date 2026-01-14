from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router


app = FastAPI(
    title="POS Backend",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    print("Application starting....")

@app.on_event("shutdown")
async def sshutdown_event():
    print("Application shutting down...")




