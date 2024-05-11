from fastapi import APIRouter, Depends, status

from src.routers.depends.use_case_depends import get_contract_use_case
from src.routers.schemas.router_schemas import ContractRequestResponse
from src.use_case.contract_use_case import ContractUseCase

contract_router = APIRouter()


@contract_router.post(
    "/contract",
    response_model=ContractRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_contract(
    contract: ContractRequestResponse,
    contract_use_case: ContractUseCase = Depends(get_contract_use_case),
):
    new_contract = await contract_use_case.create_contract(contract.to_entity())
    return new_contract
