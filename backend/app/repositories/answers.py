from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.answer import Answer, AnswerAnalysis

class AnswerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_with_analysis(
        self,
        session_id: str,
        question_id: str,
        answer_text: str | None,
        transcript: str | None,
        audio_url: str | None,
        audio_id: str | None,
        analysis_data: dict,
    ) -> tuple[Answer, AnswerAnalysis]:
        answer = Answer(
            id=f"a_{uuid4().hex[:12]}",
            session_id=session_id,
            question_id=question_id,
            answer_text=answer_text,
            transcript=transcript,
            audio_url=audio_url,
            audio_id=audio_id,
            status="processed",
        )
        self.db.add(answer)
        self.db.flush()

        analysis = AnswerAnalysis(answer_id=answer.id, **analysis_data)
        self.db.add(analysis)
        self.db.flush()
        return answer, analysis

    def get_existing_analysis_by_cache_key(self, question_id: str, answer_text: str | None) -> AnswerAnalysis | None:
        stmt = (
            select(AnswerAnalysis)
            .join(Answer, Answer.id == AnswerAnalysis.answer_id)
            .where(Answer.question_id == question_id, Answer.answer_text == answer_text)
            .order_by(Answer.created_at.desc())
            .limit(1)
        )
        return self.db.scalars(stmt).first()

    def get_analysis(self, answer_id: str) -> AnswerAnalysis | None:
        return self.db.get(AnswerAnalysis, answer_id)

    def list_for_session(self, session_id: str) -> list[Answer]:
        stmt = (
            select(Answer)
            .options(selectinload(Answer.analysis), selectinload(Answer.question))
            .where(Answer.session_id == session_id)
            .order_by(Answer.created_at)
        )
        return list(self.db.scalars(stmt).all())
