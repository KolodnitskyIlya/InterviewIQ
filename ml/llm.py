import json
import urllib.error
import urllib.request
from pydantic import ValidationError
from ml.base import RUBRIC_VERSION, AnswerAnalysisInput, AnswerAnalysisResult
from ml.prompts import ANALYSIS_SYSTEM_PROMPT, ANALYSIS_USER_PROMPT_TEMPLATE

class LLMAnalyzer:
    provider = "llm"

    def __init__(self, api_key: str, model: str, timeout_sec: int) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout_sec = timeout_sec

    def analyze(self, payload: AnswerAnalysisInput) -> AnswerAnalysisResult:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is missing")

        user_prompt = ANALYSIS_USER_PROMPT_TEMPLATE.format(
            category=payload.category,
            difficulty=payload.difficulty,
            question_title=payload.question_title,
            question_description=payload.question_description,
            has_audio=payload.has_audio,
            answer_text=(payload.transcript or payload.answer_text or "").strip() or "[empty answer]",
        )
        request_payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "answer_analysis",
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "overall_score": {"type": "integer", "minimum": 0, "maximum": 100},
                            "scores_by_category": {
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "structure": {"type": "number", "minimum": 0, "maximum": 1},
                                    "relevance": {"type": "number", "minimum": 0, "maximum": 1},
                                    "specificity": {"type": "number", "minimum": 0, "maximum": 1},
                                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                                    "completeness": {"type": "number", "minimum": 0, "maximum": 1},
                                },
                                "required": [
                                    "structure",
                                    "relevance",
                                    "specificity",
                                    "confidence",
                                    "completeness",
                                ],
                            },
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "to_improve": {"type": "array", "items": {"type": "string"}},
                            "quick_tips": {"type": "array", "items": {"type": "string"}},
                            "ideal_answer_example": {"type": "string"},
                            "explanation": {"type": "string"},
                        },
                        "required": [
                            "overall_score",
                            "scores_by_category",
                            "strengths",
                            "to_improve",
                            "quick_tips",
                            "ideal_answer_example",
                            "explanation",
                        ],
                    },
                    "strict": True,
                }
            },
        }

        raw_response = self._post_json(request_payload)
        content = self._extract_output_text(raw_response)
        try:
            data = json.loads(content)
            return AnswerAnalysisResult(
                **data,
                provider=self.provider,
                rubric_version=RUBRIC_VERSION,
                raw_response=content,
            )
        except (json.JSONDecodeError, ValidationError) as exc:
            raise RuntimeError("LLM returned invalid analysis JSON") from exc

    def _post_json(self, payload: dict) -> dict:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_sec) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI API error: {exc.code} {detail}") from exc

    def _extract_output_text(self, response: dict) -> str:
        if isinstance(response.get("output_text"), str):
            return response["output_text"]

        for item in response.get("output", []):
            for content in item.get("content", []):
                text = content.get("text")
                if isinstance(text, str):
                    return text

        raise RuntimeError("OpenAI response does not contain output text")
