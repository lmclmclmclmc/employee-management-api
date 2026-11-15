"""add employee department

Revision ID: c7cc7b70a91b
Revises: 72ad0d5a328b
Create Date: 2026-10-23 10:55:49.893078

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c7cc7b70a91b"
down_revision: Union[str, Sequence[str], None] = "72ad0d5a328b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "employees",
        sa.Column(
            "department",
            sa.Text(),
            server_default="General",
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "employees",
        "department",
    )
