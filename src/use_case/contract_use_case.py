import hashlib
import json

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
                contract_name=contract.result.ContractName,
            )
            if not await self.__contract_repository.get_contract_by_address(address):
                res = await self.__contract_repository.create_new_contract(data)
                saved_contract_data.append(res)
        return saved_contract_data

    @staticmethod
    def __check_contract_for_validation(contract_methods):
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
        return True

    async def check_contract_for_validation_and_create_tag(self, contract_address: str):

        contract_data = await self.__contract_repository.get_contract_by_address(
            contract_address, source_code=True
        )
        compiled_contract = compile_source(contract_data.source_code)
        contract_interface = compiled_contract[f"<stdin>:{contract_data.contract_name}"]
        contract_methods = {
            method["name"]: {"inputs": method["inputs"], "outputs": method["outputs"]}
            for method in contract_interface["abi"]
            if method["type"] == "function"
        }

        if self.__check_contract_for_validation(contract_methods):
            sorted_contract_methods = {
                k: contract_methods[k] for k in sorted(contract_methods)
            }

            contract_methods_json = json.dumps(
                sorted_contract_methods, separators=(",", ":"), sort_keys=True
            )

            hash_object = hashlib.sha256(contract_methods_json.encode())
            hashed_string = hash_object.hexdigest()

            await self.__contract_repository.update_contract(
                ContractDataClass(
                    contract_address=contract_address,
                    erc20_version=hashed_string,
                )
            )

            return hashed_string

    async def get_all_contact_addresses(self):
        return await self.__contract_repository.get_all_contract_addresses()
