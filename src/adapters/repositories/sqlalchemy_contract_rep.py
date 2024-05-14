from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.models.contract import Contract
from src.core.exceptions import DatabaseException
from src.dataclasses.contract_data_classes import ContractDataClass
from src.ports.repositories.contract_rep import ContractRepository


class SQLAlchemyContractRepository(ContractRepository):
    def __init__(self, db: AsyncSession):
        self.db_session = db

    @staticmethod
    def __from_model_to_dataclass(
        db_contract: Contract | None,
    ) -> ContractDataClass | None:
        if db_contract is None:
            return None
        return ContractDataClass(
            contract_address=db_contract.contract_address,
            erc20_version=db_contract.erc20_version,
        )

    async def get_contract_by_address(
        self, contract_address: str
    ) -> ContractDataClass | None:

        try:
            query = select(Contract).where(
                Contract.contract_address == contract_address
            )
            res = await self.db_session.execute(query)
            contract = res.scalar()
            user_result = self.__from_model_to_dataclass(contract)
            return user_result

        except exc.SQLAlchemyError:
            raise DatabaseException

    async def create_new_contract(
        self, contract_data: ContractDataClass
    ) -> ContractDataClass:
        try:
            new_contract = Contract(**contract_data.to_dict())
            self.db_session.add(new_contract)
            return self.__from_model_to_dataclass(new_contract)
        except exc.SQLAlchemyError:
            raise DatabaseException
