"""device tokens

Revision ID: 20260513_0004
Revises: 20260513_0003
Create Date: 2026-05-13
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "20260513_0004"
down_revision: Union[str, None] = "20260513_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "device_tokens",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("user_id", sa.String(length=32), nullable=False),
        sa.Column("token", sa.String(length=512), nullable=False),
        sa.Column("platform", sa.String(length=20), nullable=False),
        sa.Column("provider", sa.String(length=40), nullable=False),
        sa.Column("app_version", sa.String(length=40), nullable=True),
        sa.Column("device_id", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "token", name="uq_device_tokens_user_token"),
    )
    op.create_index(op.f("ix_device_tokens_user_id"), "device_tokens", ["user_id"], unique=False)

def downgrade() -> None:
    op.drop_index(op.f("ix_device_tokens_user_id"), table_name="device_tokens")
    op.drop_table("device_tokens")
