"""create_indexes

Revision ID: 002
Revises: 001
Create Date: 2024-12-10 14:41:07.782284

"""

from typing import Optional, Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Optional[str] = "001"
branch_labels: Optional[Sequence[str]] = None
depends_on: Optional[Sequence[str]] = None


def upgrade() -> None:
    op.create_index(
        index_name="uix_telegram_id_key",
        table_name="tc_records",
        columns=["telegram_id", "key"],
        unique=True,
        postgresql_include=["value"],
    )
    op.create_unique_constraint(
        constraint_name="uix_wallet_address",
        table_name="users",
        columns=["wallet_address"],
    )


def downgrade() -> None:
    op.drop_index(index_name="uix_telegram_id_key", table_name="tc_records")
    op.drop_constraint(
        constraint_name="uix_wallet_address",
        table_name="users",
        type_="unique",
    )
