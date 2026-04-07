from pydantic import BaseModel

from app.schemas.analytics import AnalyticsSessionItem


class ProgressCardData(BaseModel):
    value: int
    trend: str
    subtitle: str


class AreaToImprove(BaseModel):
    skill: str
    score: int


class ResumeSessionData(BaseModel):
    session_id: str
    question_index: int
    total_questions: int


class HomeDashboardResponse(BaseModel):
    progress_card: ProgressCardData
    areas_to_improve: list[AreaToImprove]
    recent_sessions: list[AnalyticsSessionItem]
    resume_session: ResumeSessionData | None
