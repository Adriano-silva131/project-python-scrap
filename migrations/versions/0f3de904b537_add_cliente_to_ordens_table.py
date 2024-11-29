"""add cliente to ordens_table

Revision ID: 0f3de904b537
Revises: 531a9e906cf3
Create Date: 2024-11-03 19:54:34.408662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f3de904b537'
down_revision: Union[str, None] = '531a9e906cf3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ordens', sa.Column('clientes', sa.String(length=200), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('ordens', 'clientes')
    pass
