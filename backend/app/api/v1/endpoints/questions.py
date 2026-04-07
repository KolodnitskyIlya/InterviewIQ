from fastapi import APIRouter, Query

from app.schemas.question import QuestionsResponse
from app.services.store import store


router = APIRouter(tags=["questions"])


@router.get("/questions", response_model=QuestionsResponse)
def list_questions(
    category: str | None = Query(default=None),
    difficulty: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=50),
) -> dict:
    items = store.filter_questions(category=category, difficulty=difficulty, limit=limit)
    return {"items": items}
