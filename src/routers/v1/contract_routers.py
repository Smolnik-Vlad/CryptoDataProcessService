from fastapi import APIRouter, Depends, Query, status

from src.routers.depends.use_case_depends import get_contract_use_case
from src.use_case.contract_use_case import ContractUseCase

contract_router = APIRouter()


@contract_router.post(
    "/contract",
    # response_model=list[str],
    status_code=status.HTTP_201_CREATED,
)
async def create_contract(
    list_of_contracts: list[str] = Query(None),
    contract_use_case: ContractUseCase = Depends(get_contract_use_case),
):
    new_contract = await contract_use_case.add_contracts(list_of_contracts)
    return new_contract
