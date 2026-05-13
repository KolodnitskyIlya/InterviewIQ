"""answer transcript

Revision ID: 20260513_0003
Revises: 20260512_0002
Create Date: 2026-05-13
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260513_0003"
down_revision: Union[str, None] = "20260512_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column("answers", sa.Column("transcript", sa.Text(), nullable=True))

def downgrade() -> None:
    op.drop_column("answers", "transcript")
