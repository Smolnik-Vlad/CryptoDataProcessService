from abc import ABC, abstractmethod

from src.dataclasses.contract_data_classes import ContractDataClass


class ContractRepository(ABC):

    @abstractmethod
    async def get_all_contract_addresses(self):
        pass

    @abstractmethod
    async def create_new_contract(
        self, contract_data: ContractDataClass
    ) -> ContractDataClass:
        pass

    @abstractmethod
    async def get_contract_by_address(
        self, address, source_code: bool
    ) -> ContractDataClass:
        pass
