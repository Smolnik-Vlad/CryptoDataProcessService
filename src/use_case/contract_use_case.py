

from src.dataclasses.contract_data_classes import ContractDataClass
from src.dataclasses.contract_request_dataclass import ContractRequestDataClass
from src.ports.repositories.contract_rep import ContractRepository
from src.ports.repositories.contract_request_service import \
    ContractRequestService

LIST_OF_CONTRACT_ADDRESSES = [
    "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "0xB8c77482e45F1F44dE1745F52C74426C631bDD52",
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
    "0x582d872A1B094FC48F5DE31D3B73F2D9bE47def1",
]


class ContractUseCase:
    def __init__(
        self,
        contract_repository: ContractRepository,
        request_service: ContractRequestService,
    ):
        self.__contract_repository = contract_repository
        self.__contract_request_service = request_service

    async def add_contracts(self, contract_paths: list[str] | None):
        if not contract_paths:
            contract_paths = LIST_OF_CONTRACT_ADDRESSES
        new_contracts = {
            contract_path: await self.__contract_request_service.get_new_contract(
                contract_path
            )
            for contract_path in contract_paths
        }
        filtered_contract: dict[str, ContractRequestDataClass] = dict(
            filter(lambda contr: contr[1].status == "1", new_contracts.items())
        )

        saved_contract_data = []
        for address, contract in filtered_contract.items():
            data = ContractDataClass(
                contract_address=address,
                source_code=contract.result.SourceCode,
                erc20_version=contract.result.CompilerVersion,
            )
            if not await self.__contract_repository.get_contract_by_address(address):
                res = await self.__contract_repository.create_new_contract(data)
                saved_contract_data.append(res)
        return saved_contract_data
