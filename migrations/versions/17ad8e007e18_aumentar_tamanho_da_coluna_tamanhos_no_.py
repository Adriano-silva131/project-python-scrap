"""Aumentar tamanho da coluna tamanhos_no_encaixe

Revision ID: 17ad8e007e18
Revises: f0d651cef2d9
Create Date: 2025-01-07 21:48:28.568759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '17ad8e007e18'
down_revision: Union[str, None] = 'f0d651cef2d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.alter_column(
        'camadas',
        'tamanhos_no_encaixe',
        type_=sa.String(255),
        existing_type=sa.String(100)
    )


def downgrade() -> None:
    op.alter_column(
        'camadas',
        'tamanhos_no_encaixe',
        type_=sa.String(100),
        existing_type=sa.String(255)
    )
