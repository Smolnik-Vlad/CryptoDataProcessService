from abc import ABC, abstractmethod

from src.dataclasses.contract_data_classes import ContractDataClass


class ContractRepository(ABC):

    @abstractmethod
    async def create_new_contract(
        self, contract_data: ContractDataClass
    ) -> ContractDataClass:
        pass
