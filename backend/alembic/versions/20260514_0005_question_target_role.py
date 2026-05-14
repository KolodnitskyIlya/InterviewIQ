"""add question target role

Revision ID: 20260514_0005
Revises: 20260513_0004
Create Date: 2026-05-14
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260514_0005"
down_revision: Union[str, None] = "20260513_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("questions", sa.Column("target_role", sa.String(length=120), nullable=True))
    op.create_index(op.f("ix_questions_target_role"), "questions", ["target_role"], unique=False)
    op.create_index(
        "ix_questions_role_category_difficulty",
        "questions",
        ["target_role", "category", "difficulty"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_questions_role_category_difficulty", table_name="questions")
    op.drop_index(op.f("ix_questions_target_role"), table_name="questions")
    op.drop_column("questions", "target_role")
