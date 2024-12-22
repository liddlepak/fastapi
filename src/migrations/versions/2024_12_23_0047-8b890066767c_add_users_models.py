"""add users models

Revision ID: 8b890066767c
Revises: c09e7c63c185
Create Date: 2024-12-23 00:47:50.451764

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8b890066767c"
down_revision: Union[str, None] = "c09e7c63c185"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
