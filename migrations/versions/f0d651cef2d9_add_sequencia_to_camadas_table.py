"""add_sequencia_to_camadas_table

Revision ID: f0d651cef2d9
Revises: dc6dc512fb90
Create Date: 2024-11-28 22:28:49.897668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f0d651cef2d9'
down_revision: Union[str, None] = 'dc6dc512fb90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('camadas', sa.Column('sequencia', sa.Integer(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('camadas', 'sequencia')
    pass

