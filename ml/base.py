from typing import Protocol
from pydantic import BaseModel, Field

RUBRIC_VERSION = "rubric_v1"
RUBRIC_WEIGHTS = {
    "structure": 0.20,
    "relevance": 0.25,
    "specificity": 0.25,
    "confidence": 0.10,
    "completeness": 0.20,
}

class AnswerAnalysisInput(BaseModel):
    answer_text: str | None = None
    question_title: str
    question_description: str
    category: str
    difficulty: str
    has_audio: bool = False
    audio_url: str | None = None
    transcript: str | None = None

class AnswerAnalysisResult(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    scores_by_category: dict[str, float]
    strengths: list[str]
    to_improve: list[str]
    quick_tips: list[str]
    ideal_answer_example: str
    explanation: str
    provider: str
    rubric_version: str = RUBRIC_VERSION
    raw_response: str | None = None
    error_message: str | None = None
    latency_ms: int = 0

class AnswerAnalyzer(Protocol):
    def analyze(self, payload: AnswerAnalysisInput) -> AnswerAnalysisResult:
        ...
