"""1

Revision ID: 6a271e9e96b3
Revises: 
Create Date: 2024-05-11 21:39:09.318444

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6a271e9e96b3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contract",
        sa.Column("contract_address", sa.String(), nullable=False),
        sa.Column("source_code", sa.Text(), nullable=False),
        sa.Column("erc20_version", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("contract_address"),
        sa.UniqueConstraint("contract_address"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("contract")
    # ### end Alembic commands ###
