from fastapi import FastAPI

from src.routers.general_router import v1_router

app = FastAPI()


@app.get("/health")
async def root():
    return True


app.include_router(v1_router, prefix="/v1")
