from fastapi import APIRouter, Depends, status

from src.routers.depends.use_case_depends import get_contract_use_case
from src.use_case.contract_use_case import ContractUseCase

contract_router = APIRouter()


@contract_router.post(
    "/contract",
    # response_model=list[str],
    status_code=status.HTTP_201_CREATED,
)
async def create_contract(
    # list_of_contracts: list[str] = Query(None),
    contract_use_case: ContractUseCase = Depends(get_contract_use_case),
):
    new_contract = await contract_use_case.add_contracts()
    return new_contract


@contract_router.get("/contract-addresses", status_code=status.HTTP_200_OK)
async def get_contract_addresses(
    contract_use_case: ContractUseCase = Depends(get_contract_use_case),
):
    addresses = await contract_use_case.get_all_contact_addresses()
    return addresses


@contract_router.get("/check_contract", status_code=status.HTTP_200_OK)
async def check_contract(
    contract_address: str,
    contract_use_case: ContractUseCase = Depends(get_contract_use_case),
):
    result = await contract_use_case.check_contract_for_validation_and_create_tag(
        contract_address
    )
    return {"message": result}
