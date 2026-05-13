import json
import os
from pathlib import Path
from gigachat import GigaChat
from pydantic import ValidationError
from ml.base import RUBRIC_VERSION, AnswerAnalysisInput, AnswerAnalysisResult
from ml.prompts import ANALYSIS_SYSTEM_PROMPT, ANALYSIS_USER_PROMPT_TEMPLATE

REQUIRED_SCORE_KEYS = ["structure", "relevance", "specificity", "confidence", "completeness"]

class GigaChatAnalyzer:
    provider = "gigachat"

    def __init__(
        self,
        credentials: str,
        model: str = "GigaChat",
        scope: str = "GIGACHAT_API_PERS",
        verify_ssl_certs: bool = False,
        timeout_sec: int = 20,
    ) -> None:
        self.credentials = credentials
        self.model = model
        self.scope = scope
        self.verify_ssl_certs = verify_ssl_certs
        self.timeout_sec = timeout_sec

    def analyze(self, payload: AnswerAnalysisInput) -> AnswerAnalysisResult:
        if not self.credentials:
            raise RuntimeError("GIGACHAT_CREDENTIALS is missing")

        user_prompt = ANALYSIS_USER_PROMPT_TEMPLATE.format(
            category=payload.category,
            difficulty=payload.difficulty,
            question_title=payload.question_title,
            question_description=payload.question_description,
            has_audio=payload.has_audio,
            answer_text=(payload.transcript or payload.answer_text or "").strip() or "[empty answer]",
        )
        strict_prompt = (
            f"{user_prompt}\n\n"
            "CRITICAL JSON CONTRACT:\n"
            "Return exactly one JSON object. Required key name is scores_by_category, not by_category.\n"
            "scores_by_category must contain structure, relevance, specificity, confidence, completeness.\n"
            "Each category score must be a float from 0.0 to 1.0, not percent.\n"
            "Do not wrap JSON in markdown."
        )

        with GigaChat(
            credentials=self.credentials,
            scope=self.scope,
            model=self.model,
            verify_ssl_certs=self.verify_ssl_certs,
            timeout=self.timeout_sec,
        ) as giga:
            response = giga.chat(
                {
                    "messages": [
                        {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                        {"role": "user", "content": strict_prompt},
                    ],
                    "temperature": 0.0,
                }
            )

        content = response.choices[0].message.content
        try:
            data = self._normalize_response(json.loads(self._extract_json(content)))
            return AnswerAnalysisResult(
                **data,
                provider=self.provider,
                rubric_version=RUBRIC_VERSION,
                raw_response=content,
            )
        except (json.JSONDecodeError, ValidationError) as exc:
            raise RuntimeError("GigaChat returned invalid analysis JSON") from exc

    def _extract_json(self, content: str) -> str:
        stripped = content.strip()
        if stripped.startswith("```"):
            stripped = stripped.strip("`")
            if stripped.lower().startswith("json"):
                stripped = stripped[4:].strip()

        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return stripped
        return stripped[start : end + 1]

    def _normalize_response(self, data: dict) -> dict:
        scores = data.get("scores_by_category") or data.get("by_category") or data.get("category_scores")
        if not isinstance(scores, dict):
            scores = {}

        normalized_scores = {}
        for key in REQUIRED_SCORE_KEYS:
            raw_value = scores.get(key, 0.0)
            try:
                value = float(raw_value)
            except (TypeError, ValueError):
                value = 0.0
            if value > 1.0:
                value = value / 100.0
            normalized_scores[key] = round(max(0.0, min(1.0, value)), 2)

        data["scores_by_category"] = normalized_scores
        data["overall_score"] = int(max(0, min(100, int(data.get("overall_score", 0)))))

        for key in ["strengths", "to_improve", "quick_tips"]:
            value = data.get(key)
            if isinstance(value, str):
                data[key] = [value]
            elif not isinstance(value, list):
                data[key] = []

        data.setdefault("strengths", ["Relevant answer direction"])
        data.setdefault("to_improve", ["Add more specific details"])
        data.setdefault("quick_tips", ["Use a clear structure and finish with impact"])
        data.setdefault("ideal_answer_example", "Start with the approach, explain trade-offs, and finish with measurable impact.")
        data.setdefault("explanation", "GigaChat analysis normalized to the InterviewIQ rubric.")
        return data

def _load_local_env() -> None:
    api_env = Path(__file__).resolve().parents[1] / "backend" / "api.env"
    if not api_env.exists():
        return

    for line in api_env.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())

def main() -> None:
    _load_local_env()
    credentials = os.getenv("GIGACHAT_CREDENTIALS", "")
    if not credentials:
        print("GIGACHAT_CREDENTIALS is empty. Add it to backend/api.env or environment variables.")
        return

    payload = AnswerAnalysisInput(
        answer_text="First, I would clarify requirements, compare trade-offs, and measure impact by 25%.",
        question_title="Design a notification service",
        question_description="Cover architecture, retries, delivery guarantees, and monitoring.",
        category="system-design",
        difficulty="medium",
        has_audio=False,
    )
    result = GigaChatAnalyzer(
        credentials=credentials,
        model=os.getenv("GIGACHAT_MODEL", "GigaChat"),
        scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
        verify_ssl_certs=os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "false").lower() == "true",
        timeout_sec=int(os.getenv("ANALYZER_TIMEOUT_SEC", "20")),
    ).analyze(payload)
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
