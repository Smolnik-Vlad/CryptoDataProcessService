from fastapi import APIRouter

from src.routers.v1.contract_routers import contract_router

v1_router = APIRouter()
v1_router.include_router(contract_router, prefix="/contract", tags=["contract"])
