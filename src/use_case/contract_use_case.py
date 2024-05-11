from src.dataclasses.contract_data_classes import ContractDataClass
from src.ports.repositories.contract_rep import ContractRepository


class ContractUseCase:
    def __init__(self, contract_repository: ContractRepository):
        self.__contract_repository = contract_repository

    async def create_contract(self, contract: ContractDataClass):
        new_contract = await self.__contract_repository.create_new_contract(contract)
        return new_contract
