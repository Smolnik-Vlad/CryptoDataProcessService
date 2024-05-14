from dataclasses import dataclass


@dataclass
class ResultDataClass:
    SourceCode: str
    ABI: str
    ContractName: str
    CompilerVersion: str
    OptimizationUsed: str
    Runs: str
    ConstructorArguments: str
    EVMVersion: str
    Library: str
    Proxy: str
    Implementation: str
    SwarmSource: str
    LicenseType: str


@dataclass
class ContractRequestDataClass:
    status: str
    message: str
    result: list[dict] | ResultDataClass

    def __post_init__(self):
        self.result = ResultDataClass(**self.result[0])
