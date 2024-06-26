from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Contract(Base):
    __tablename__ = "contract"
    contract_address: Mapped[str] = mapped_column(
        String[100], primary_key=True, unique=True, nullable=False
    )
    source_code = mapped_column(Text, nullable=False)
    erc20_version: Mapped[str] = mapped_column(String(255), nullable=True)
    contract_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
