"""adicionar_coluna_timestamp_to_ordens

Revision ID: 531a9e906cf3
Revises: b8efe47acebe
Create Date: 2024-09-21 15:53:33.228383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '531a9e906cf3'
down_revision: Union[str, None] = 'b8efe47acebe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ordens', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now(), nullable=False))
    op.add_column('ordens', sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))


def downgrade() -> None:
    op.drop_column('ordens', 'created_at')
    op.drop_column('ordens', 'updated_at')
