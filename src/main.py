from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.core.exceptions import CustomBaseException
from src.routers.general_router import v1_router

app = FastAPI()


@app.exception_handler(CustomBaseException)
async def custom_exception_handler(request, exc):
    error_class_name = exc.__class__.__name__
    error_detail = f"Custom error: {error_class_name}"
    return JSONResponse(status_code=exc.status_code, content={"detail": error_detail})


@app.get("/health")
async def root():
    return True


app.include_router(v1_router, prefix="/v1")
