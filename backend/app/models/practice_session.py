from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(30), nullable=False)
    time_limit_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    question_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), index=True, nullable=False, default="created")
    current_question_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="sessions")
    questions = relationship(
        "PracticeSessionQuestion",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="PracticeSessionQuestion.position",
    )
    answers = relationship("Answer", back_populates="session", cascade="all, delete-orphan")

class PracticeSessionQuestion(Base):
    __tablename__ = "practice_session_questions"
    __table_args__ = (
        UniqueConstraint("session_id", "position", name="uq_session_question_position"),
    )

    session_id: Mapped[str] = mapped_column(ForeignKey("practice_sessions.id", ondelete="CASCADE"), primary_key=True)
    question_id: Mapped[str] = mapped_column(ForeignKey("questions.id", ondelete="RESTRICT"), primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    session = relationship("PracticeSession", back_populates="questions")
    question = relationship("Question")
