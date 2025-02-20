"""adicionando a coluna de spread

Revision ID: 94b978755b37
Revises: 17ad8e007e18
Create Date: 2025-02-16 18:28:09.675993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "94b978755b37"
down_revision: Union[str, None] = "17ad8e007e18"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("camadas", sa.Column("spread", sa.Float, nullable=True))


def downgrade() -> None:
    op.drop_column("camadas", "spread")
