from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("practice_sessions.id", ondelete="CASCADE"), index=True)
    question_id: Mapped[str] = mapped_column(ForeignKey("questions.id", ondelete="RESTRICT"), index=True)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    audio_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    audio_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="processed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    session = relationship("PracticeSession", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    analysis = relationship("AnswerAnalysis", back_populates="answer", cascade="all, delete-orphan", uselist=False)

class AnswerAnalysis(Base):
    __tablename__ = "answer_analysis"

    answer_id: Mapped[str] = mapped_column(ForeignKey("answers.id", ondelete="CASCADE"), primary_key=True)
    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)
    scores_by_category: Mapped[dict] = mapped_column(JSON, nullable=False)
    strengths: Mapped[list] = mapped_column(JSON, nullable=False)
    to_improve: Mapped[list] = mapped_column(JSON, nullable=False)
    quick_tips: Mapped[list] = mapped_column(JSON, nullable=False)
    ideal_answer_example: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider: Mapped[str] = mapped_column(String(40), nullable=False, default="baseline")
    rubric_version: Mapped[str] = mapped_column(String(40), nullable=False, default="rubric_v1")
    raw_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    answer = relationship("Answer", back_populates="analysis")
