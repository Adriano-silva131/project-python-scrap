"""create_camada_table

Revision ID: b8efe47acebe
Revises: 8a9057cdd58a
Create Date: 2024-09-04 22:29:37.748282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8efe47acebe'
down_revision: Union[str, None] = '8a9057cdd58a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_table(
        'camadas',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ordem_id', sa.Integer(), sa.ForeignKey('ordens.id'), nullable=True),
        sa.Column('camada', sa.String(length=50), nullable=True),
        sa.Column('tamanhos_no_encaixe', sa.String(length=100), nullable=True),
        sa.Column('quantidade_enfesto', sa.Text(), nullable=True),
        sa.Column('tecido', sa.Text(), nullable=True),
        sa.Column('tipo', sa.String(length=50), nullable=True),
        sa.Column('largura_cm', sa.String(length=50), nullable=True),
        sa.Column('comprimento_m', sa.String(length=50), nullable=True),
        sa.Column('tecido_total_m', sa.Text(), nullable=True),
        sa.Column('consumo_total_tecido_kg', sa.Text(), nullable=True),
        sa.Column('perimetro_de_corte_m', sa.String(length=50), nullable=True),
        sa.Column('largura_encolhimento', sa.String(length=10), nullable=True),
        sa.Column('comprimento_encolhimento', sa.String(length=10), nullable=True),
        sa.Column('gap_de_peca_cm', sa.String(length=50), nullable=True),
        sa.Column('total_de_produtos', sa.Integer(), nullable=True),
        sa.Column('numeracao_do_produto', sa.String(length=50), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('camadas')
