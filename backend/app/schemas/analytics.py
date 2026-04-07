from pydantic import BaseModel


class OverviewResponse(BaseModel):
    readiness_score: int
    average_score: int
    trend_percent: int


class SkillItem(BaseModel):
    name: str
    score: int
    change: int


class SkillsResponse(BaseModel):
    items: list[SkillItem]


class WeeklyPoint(BaseModel):
    day: str
    score: int


class WeeklyProgressResponse(BaseModel):
    points: list[WeeklyPoint]


class AnalyticsSessionItem(BaseModel):
    session_id: str
    category: str
    score: int
    completed_at: str | None
    questions_count: int
    duration_min: int


class AnalyticsSessionsResponse(BaseModel):
    items: list[AnalyticsSessionItem]
    total: int
    page: int
    page_size: int
