"""create_ordem_table

Revision ID: 8a9057cdd58a
Revises: ac4e9ecfd6cf
Create Date: 2024-09-04 22:14:41.064858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a9057cdd58a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ordens',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ordem', sa.String(length=50), nullable=True),
        sa.Column('numero_pecas', sa.Integer(), nullable=True),
        sa.Column('quantidade_total', sa.String(length=50), nullable=True),
        sa.Column('product_type', sa.String(length=50), nullable=True),
        sa.Column('eficiencia', sa.Numeric(precision=10, scale=4),nullable=True),
        sa.Column('nome_arquivo', sa.String(length=200), nullable=False)          
    )

def downgrade() -> None:
    op.drop_table('ordens')
