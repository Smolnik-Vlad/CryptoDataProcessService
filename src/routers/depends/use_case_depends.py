from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.engines.async_client.async_client import get_async_client
from src.adapters.repositories.contract_httpx_service import \
    ContractHttpxService
from src.adapters.repositories.sqlalchemy_contract_rep import \
    SQLAlchemyContractRepository
from src.ports.repositories.contract_rep import ContractRepository
from src.ports.repositories.contract_request_service import \
    ContractRequestService
from src.routers.depends.database_depends import get_db
from src.use_case.contract_use_case import ContractUseCase


def get_contract_repository(db: AsyncSession = Depends(get_db)) -> ContractRepository:
    return SQLAlchemyContractRepository(db)


def get_contract_service(http_client=Depends(get_async_client)):
    return ContractHttpxService(http_client)


def get_contract_use_case(
    contract_repository: ContractRepository = Depends(get_contract_repository),
    contract_service: ContractRequestService = Depends(get_contract_service),
):
    return ContractUseCase(contract_repository, contract_service)
