"""add product to ordens table

Revision ID: dc6dc512fb90
Revises: 0f3de904b537
Create Date: 2024-11-19 22:45:27.486311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dc6dc512fb90'
down_revision: Union[str, None] = '0f3de904b537'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ordens', sa.Column('product', sa.String(length=200), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('ordens', 'product')
    pass
