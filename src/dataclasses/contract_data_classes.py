from abc import ABC
from dataclasses import dataclass


class DataClassFunctionality(ABC):
    def to_dict(self, exclude_none=True) -> dict:
        if exclude_none:
            return {k: v for k, v in self.__dict__.items() if v is not None}
        else:
            return self.__dict__.copy()


@dataclass
class ContractDataClass(DataClassFunctionality):
    contract_address: str | None = None
    contract_name: str | None = None
    erc20_version: str | None = None
    source_code: str | None = None
