from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repositories.sqlalchemy_contract_rep import \
    SQLAlchemyContractRepository
from src.ports.repositories.contract_rep import ContractRepository
from src.routers.depends.database_depends import get_db
from src.use_case.contract_use_case import ContractUseCase


def get_contract_repository(db: AsyncSession = Depends(get_db)) -> ContractRepository:
    return SQLAlchemyContractRepository(db)


def get_contract_use_case(
    contract_repository: ContractRepository = Depends(get_contract_repository),
):
    return ContractUseCase(contract_repository)
