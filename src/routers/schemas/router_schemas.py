from pydantic import BaseModel, ConfigDict

from src.dataclasses.contract_data_classes import ContractDataClass


class ContractRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    contract_address: str
    source_code: str
    erc20_version: str
    contract_name: str

    def to_entity(self):
        return ContractDataClass(
            contract_address=self.contract_address,
            source_code=self.source_code,
            erc20_version=self.erc20_version,
            contract_name=self.contract_name,
        )
