"""rooms migration

Revision ID: 6446212f82bf
Revises: 92e3ff92dc72
Create Date: 2024-12-11 18:11:50.635835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '6446212f82bf'
down_revision: Union[str, None] = '92e3ff92dc72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hotel_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('rooms')
