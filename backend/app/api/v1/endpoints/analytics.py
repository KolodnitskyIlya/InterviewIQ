from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user
from app.schemas.analytics import (
    AnalyticsSessionsResponse,
    OverviewResponse,
    SkillsResponse,
    WeeklyProgressResponse,
)
from app.services.store import store


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=OverviewResponse)
def analytics_overview(user: dict = Depends(get_current_user)) -> dict:
    return store.analytics_overview(user_id=user["id"])


@router.get("/skills", response_model=SkillsResponse)
def analytics_skills(user: dict = Depends(get_current_user)) -> dict:
    return {"items": store.analytics_skills(user_id=user["id"])}


@router.get("/weekly-progress", response_model=WeeklyProgressResponse)
def analytics_weekly_progress(user: dict = Depends(get_current_user)) -> dict:
    return {"points": store.analytics_weekly_progress(user_id=user["id"])}


@router.get("/sessions", response_model=AnalyticsSessionsResponse)
def analytics_sessions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user: dict = Depends(get_current_user),
) -> dict:
    all_items = store.analytics_sessions(user_id=user["id"])
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": all_items[start:end],
        "total": len(all_items),
        "page": page,
        "page_size": page_size,
    }
