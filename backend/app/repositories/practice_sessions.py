from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.practice_session import PracticeSession, PracticeSessionQuestion
from app.models.question import Question

class PracticeSessionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        user_id: str,
        category: str,
        difficulty: str,
        time_limit_sec: int,
        questions: list[Question],
    ) -> PracticeSession:
        session = PracticeSession(
            id=f"s_{uuid4().hex[:12]}",
            user_id=user_id,
            category=category,
            difficulty=difficulty,
            time_limit_sec=time_limit_sec,
            question_count=len(questions),
            status="created",
            current_question_index=0,
        )
        session.questions = [
            PracticeSessionQuestion(question_id=question.id, position=index)
            for index, question in enumerate(questions)
        ]
        self.db.add(session)
        self.db.flush()
        return session

    def get_for_user(self, user_id: str, session_id: str) -> PracticeSession | None:
        stmt = (
            select(PracticeSession)
            .options(
                selectinload(PracticeSession.questions).selectinload(PracticeSessionQuestion.question),
                selectinload(PracticeSession.answers),
            )
            .where(PracticeSession.id == session_id, PracticeSession.user_id == user_id)
        )
        return self.db.scalars(stmt).first()

    def start(self, session: PracticeSession) -> PracticeSession:
        if session.status == "created":
            session.status = "in_progress"
            session.started_at = datetime.now(timezone.utc)
            self.db.flush()
        return session

    def finish(self, session: PracticeSession) -> PracticeSession:
        now = datetime.now(timezone.utc)
        session.status = "finished"
        if session.started_at is None:
            session.started_at = now
        session.finished_at = now
        self.db.flush()
        return session

    def move_next(self, session: PracticeSession) -> Question | None:
        if session.current_question_index + 1 >= len(session.questions):
            return None
        session.current_question_index += 1
        self.db.flush()
        return self.current_question(session)

    def current_question(self, session: PracticeSession) -> Question | None:
        if session.current_question_index >= len(session.questions):
            return None
        return session.questions[session.current_question_index].question

    def list_finished_for_user(self, user_id: str) -> list[PracticeSession]:
        stmt = (
            select(PracticeSession)
            .options(
                selectinload(PracticeSession.questions),
                selectinload(PracticeSession.answers),
            )
            .where(PracticeSession.user_id == user_id, PracticeSession.status == "finished")
            .order_by(PracticeSession.finished_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def latest_active_for_user(self, user_id: str) -> PracticeSession | None:
        stmt = (
            select(PracticeSession)
            .where(
                PracticeSession.user_id == user_id,
                PracticeSession.status.in_(["created", "in_progress"]),
            )
            .order_by(PracticeSession.created_at.desc())
            .limit(1)
        )
        return self.db.scalars(stmt).first()
