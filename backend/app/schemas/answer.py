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
    explanation: str | None = None
    provider: str | None = None
    rubric_version: str | None = None
    error_message: str | None = None
    latency_ms: int | None = None

class AudioUploadRequest(BaseModel):
    question_id: str
    file_name: str
    content_type: str = "audio/mp4"
    audio_base64: str

class AudioUploadResponse(BaseModel):
    audio_id: str
    audio_url: str
    content_type: str
