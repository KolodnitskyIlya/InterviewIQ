from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.question import Question

class QuestionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_questions(
        self,
        category: str | None = None,
        difficulty: str | None = None,
        target_role: str | None = None,
        limit: int = 10,
    ) -> list[Question]:
        stmt = select(Question).order_by(func.random()).limit(limit)
        if category:
            stmt = stmt.where(Question.category == category)
        if difficulty:
            stmt = stmt.where(Question.difficulty == difficulty)
        if target_role:
            stmt = stmt.where(Question.target_role == target_role)
        return list(self.db.scalars(stmt).all())

    def get(self, question_id: str) -> Question | None:
        return self.db.get(Question, question_id)

    def upsert_many(self, questions: list[dict]) -> int:
        added = 0
        for item in questions:
            question = self.db.get(Question, item["id"])
            if question is None:
                question = Question(**item)
                self.db.add(question)
                added += 1
                continue

            question.category = item["category"]
            question.difficulty = item["difficulty"]
            question.target_role = item.get("target_role")
            question.title = item["title"]
            question.description = item["description"]
        self.db.flush()
        return added
