import solcx
from solcx import compile_source

from src.dataclasses.contract_data_classes import ContractDataClass
from src.dataclasses.contract_request_dataclass import ContractRequestDataClass
from src.ports.repositories.contract_rep import ContractRepository
from src.ports.repositories.contract_request_service import \
    ContractRequestService
from src.use_case.constants import erc20_methods

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
                contract_name=contract.result.ContractName,
            )
            if not await self.__contract_repository.get_contract_by_address(address):
                res = await self.__contract_repository.create_new_contract(data)
                saved_contract_data.append(res)
        return saved_contract_data

    async def check_contract_for_validation(self, contract_address: str):

        contract_data = await self.__contract_repository.get_contract_by_address(
            contract_address, source_code=True
        )
        print(solcx.get_solc_version())
        compiled_contract = compile_source(contract_data.source_code)
        contract_interface = compiled_contract[f"<stdin>:{contract_data.contract_name}"]
        contract_methods = {
            method["name"]: {"inputs": method["inputs"], "outputs": method["outputs"]}
            for method in contract_interface["abi"]
            if method["type"] == "function"
        }

        for method_name, method_params in erc20_methods.items():
            if method_name not in contract_methods:
                return False

            if len(contract_methods[method_name]["inputs"]) != len(
                method_params["inputs"]
            ) or len(contract_methods[method_name]["outputs"]) != len(
                method_params["outputs"]
            ):
                return False

            for i in range(len(method_params["inputs"])):
                if (
                    contract_methods[method_name]["inputs"][i]["type"]
                    != method_params["inputs"][i]["type"]
                ):
                    return False

            for i in range(len(method_params["outputs"])):
                if (
                    contract_methods[method_name]["outputs"][i]["type"]
                    != method_params["outputs"][i]["type"]
                ):
                    return False
        print("It is possible")
        return True
        # print(solcx.get_installable_solc_versions())

    async def get_all_contact_addresses(self):
        return await self.__contract_repository.get_all_contract_addresses()
