from pydantic import BaseModel, Field


class PracticeConfigResponse(BaseModel):
    categories: list[str]
    difficulties: list[str]
    time_limits_sec: list[int]
    question_count_options: list[int]


class CreateSessionRequest(BaseModel):
    category: str
    difficulty: str
    time_limit_sec: int = Field(ge=15, le=600)
    question_count: int = Field(ge=1, le=20)


class SessionStateResponse(BaseModel):
    id: str
    status: str
    category: str
    difficulty: str
    time_limit_sec: int
    question_count: int
    current_question_index: int
    created_at: str
    started_at: str | None
    finished_at: str | None


class SessionResultItem(BaseModel):
    answer_id: str
    question_id: str
    question_title: str
    score: int


class SessionResultsResponse(BaseModel):
    session_id: str
    status: str
    average_score: int
    questions_answered: int
    question_results: list[SessionResultItem]
    finished_at: str | None
