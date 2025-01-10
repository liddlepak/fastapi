"""update model

Revision ID: 36d3062bcec7
Revises: 66817a96e38e
Create Date: 2025-01-09 23:53:43.249651

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "36d3062bcec7"
down_revision: Union[str, None] = "66817a96e38e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("bookings", sa.Column("room_id", sa.Integer(), nullable=False))
    op.drop_constraint("bookings_rooms_id_fkey", "bookings", type_="foreignkey")
    op.create_foreign_key(None, "bookings", "rooms", ["room_id"], ["id"])
    op.drop_column("bookings", "rooms_id")


def downgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column("rooms_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.create_foreign_key(
        "bookings_rooms_id_fkey", "bookings", "rooms", ["rooms_id"], ["id"]
    )
    op.drop_column("bookings", "room_id")
