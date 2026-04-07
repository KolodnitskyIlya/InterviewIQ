from pydantic import BaseModel

class SubmitAnswerRequest(BaseModel):
    question_id: str
    answer_text: str | None = None
    audio_url: str | None = None
    audio_id: str | None = None


class SubmitAnswerResponse(BaseModel):
    answer_id: str
    session_id: str
    question_id: str
    status: str

class AnswerAnalysisResponse(BaseModel):
    answer_id: str
    overall_score: int
    scores_by_category: dict[str, float]
    strengths: list[str]
    to_improve: list[str]
    quick_tips: list[str]
    ideal_answer_example: str
