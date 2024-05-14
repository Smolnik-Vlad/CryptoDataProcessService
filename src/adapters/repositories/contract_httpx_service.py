from httpx import AsyncClient

from src.core.settings import settings
from src.dataclasses.contract_request_dataclass import ContractRequestDataClass
from src.ports.repositories.contract_request_service import \
    ContractRequestService


class ContractHttpxService(ContractRequestService):

    def __init__(self, async_client: AsyncClient):
        self.async_client = async_client
        self.__url = "https://api.etherscan.io/api"
        self.__apikey = settings.ETHERSCAN_KEY

    async def get_new_contract(self, address: str) -> ContractRequestDataClass:
        query_params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
            "apikey": self.__apikey,
        }
        response = await self.async_client.get(self.__url, params=query_params)
        contr_json = response.json()
        return ContractRequestDataClass(**contr_json)
