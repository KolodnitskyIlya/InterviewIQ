"""initial schema

Revision ID: 20260509_0001
Revises:
Create Date: 2026-05-09
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("target_role", sa.String(length=120), nullable=True),
        sa.Column("experience_level", sa.String(length=40), nullable=True),
        sa.Column("onboarding_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "questions",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("difficulty", sa.String(length=30), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_questions_category"), "questions", ["category"], unique=False)
    op.create_index(op.f("ix_questions_difficulty"), "questions", ["difficulty"], unique=False)
    op.create_index("ix_questions_category_difficulty", "questions", ["category", "difficulty"], unique=False)

    op.create_table(
        "auth_tokens",
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.String(length=32), nullable=False),
        sa.Column("token_type", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("token"),
    )
    op.create_index(op.f("ix_auth_tokens_user_id"), "auth_tokens", ["user_id"], unique=False)

    op.create_table(
        "practice_sessions",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("user_id", sa.String(length=32), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("difficulty", sa.String(length=30), nullable=False),
        sa.Column("time_limit_sec", sa.Integer(), nullable=False),
        sa.Column("question_count", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("current_question_index", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_practice_sessions_status"), "practice_sessions", ["status"], unique=False)
    op.create_index(op.f("ix_practice_sessions_user_id"), "practice_sessions", ["user_id"], unique=False)

    op.create_table(
        "practice_session_questions",
        sa.Column("session_id", sa.String(length=32), nullable=False),
        sa.Column("question_id", sa.String(length=32), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["session_id"], ["practice_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("session_id", "question_id"),
        sa.UniqueConstraint("session_id", "position", name="uq_session_question_position"),
    )

    op.create_table(
        "answers",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("session_id", sa.String(length=32), nullable=False),
        sa.Column("question_id", sa.String(length=32), nullable=False),
        sa.Column("answer_text", sa.Text(), nullable=True),
        sa.Column("audio_url", sa.String(length=1024), nullable=True),
        sa.Column("audio_id", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["session_id"], ["practice_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_answers_question_id"), "answers", ["question_id"], unique=False)
    op.create_index(op.f("ix_answers_session_id"), "answers", ["session_id"], unique=False)

    op.create_table(
        "answer_analysis",
        sa.Column("answer_id", sa.String(length=32), nullable=False),
        sa.Column("overall_score", sa.Integer(), nullable=False),
        sa.Column("scores_by_category", sa.JSON(), nullable=False),
        sa.Column("strengths", sa.JSON(), nullable=False),
        sa.Column("to_improve", sa.JSON(), nullable=False),
        sa.Column("quick_tips", sa.JSON(), nullable=False),
        sa.Column("ideal_answer_example", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["answer_id"], ["answers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("answer_id"),
    )

def downgrade() -> None:
    op.drop_table("answer_analysis")
    op.drop_index(op.f("ix_answers_session_id"), table_name="answers")
    op.drop_index(op.f("ix_answers_question_id"), table_name="answers")
    op.drop_table("answers")
    op.drop_table("practice_session_questions")
    op.drop_index(op.f("ix_practice_sessions_user_id"), table_name="practice_sessions")
    op.drop_index(op.f("ix_practice_sessions_status"), table_name="practice_sessions")
    op.drop_table("practice_sessions")
    op.drop_index(op.f("ix_auth_tokens_user_id"), table_name="auth_tokens")
    op.drop_table("auth_tokens")
    op.drop_index("ix_questions_category_difficulty", table_name="questions")
    op.drop_index(op.f("ix_questions_difficulty"), table_name="questions")
    op.drop_index(op.f("ix_questions_category"), table_name="questions")
    op.drop_table("questions")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
