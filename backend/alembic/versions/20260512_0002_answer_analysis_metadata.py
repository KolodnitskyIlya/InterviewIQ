"""answer analysis metadata

Revision ID: 20260512_0002
Revises: 20260509_0001
Create Date: 2026-05-12
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260512_0002"
down_revision: Union[str, None] = "20260509_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("answer_analysis", sa.Column("explanation", sa.Text(), nullable=True))
    op.add_column(
        "answer_analysis",
        sa.Column("provider", sa.String(length=40), server_default="baseline", nullable=False),
    )
    op.add_column(
        "answer_analysis",
        sa.Column("rubric_version", sa.String(length=40), server_default="rubric_v1", nullable=False),
    )
    op.add_column("answer_analysis", sa.Column("raw_response", sa.Text(), nullable=True))
    op.add_column("answer_analysis", sa.Column("error_message", sa.Text(), nullable=True))
    op.add_column("answer_analysis", sa.Column("latency_ms", sa.Integer(), nullable=True))
    op.alter_column("answer_analysis", "provider", server_default=None)
    op.alter_column("answer_analysis", "rubric_version", server_default=None)


def downgrade() -> None:
    op.drop_column("answer_analysis", "latency_ms")
    op.drop_column("answer_analysis", "error_message")
    op.drop_column("answer_analysis", "raw_response")
    op.drop_column("answer_analysis", "rubric_version")
    op.drop_column("answer_analysis", "provider")
    op.drop_column("answer_analysis", "explanation")
