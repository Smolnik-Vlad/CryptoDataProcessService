from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.models.contract import Contract
from src.core.exceptions import DatabaseException
from src.dataclasses.contract_data_classes import ContractDataClass
from src.ports.repositories.contract_rep import ContractRepository


class SQLAlchemyContractRepository(ContractRepository):
    def __init__(self, db: AsyncSession):
        self.db_session = db

    @staticmethod
    def __from_model_to_database(
        db_contract: Contract | None,
    ) -> ContractDataClass | None:
        if db_contract is None:
            return None
        return ContractDataClass(
            contract_address=db_contract.contract_address,
            source_code=db_contract.source_code,
            erc20_version=db_contract.erc20_version,
        )

    async def create_new_contract(
        self, contract_data: ContractDataClass
    ) -> ContractDataClass:
        try:
            new_contract = Contract(**contract_data.to_dict())
            self.db_session.add(new_contract)
            # await self.db_session.commit()
            # await self.db_session.flush()
            # await self.db_session.commit()

            return self.__from_model_to_database(new_contract)
        except exc.SQLAlchemyError:
            raise DatabaseException
