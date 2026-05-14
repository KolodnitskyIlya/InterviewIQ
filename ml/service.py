import hashlib
import logging
import re
import time
from ml.base import RUBRIC_VERSION, AnswerAnalysisInput, AnswerAnalysisResult
from ml.baseline import BaselineAnalyzer
from ml.gigachat import GigaChatAnalyzer

logger = logging.getLogger("interviewiq.analyzer")

class AnalyzerService:
    def __init__(
        self,
        provider: str = "baseline",
        gigachat_credentials: str = "",
        gigachat_model: str = "GigaChat",
        gigachat_scope: str = "GIGACHAT_API_PERS",
        gigachat_verify_ssl_certs: bool = False,
        analyzer_timeout_sec: int = 20,
        max_answer_chars: int = 6000,
    ) -> None:
        self.provider = provider
        self.max_answer_chars = max_answer_chars
        self.baseline = BaselineAnalyzer()
        self.gigachat = GigaChatAnalyzer(
            credentials=gigachat_credentials,
            model=gigachat_model,
            scope=gigachat_scope,
            verify_ssl_certs=gigachat_verify_ssl_certs,
            timeout_sec=analyzer_timeout_sec,
        )
        self._cache: dict[str, AnswerAnalysisResult] = {}

    def analyze(self, payload: AnswerAnalysisInput, session_id: str | None = None) -> AnswerAnalysisResult:
        safe_payload = payload.model_copy(
            update={
                "answer_text": self._limit_text(payload.answer_text),
                "transcript": self._limit_text(payload.transcript),
            }
        )
        cache_key = self._cache_key(safe_payload)
        cached = self._cache.get(cache_key)
        if cached:
            return cached.model_copy(update={"latency_ms": 0})

        started = time.perf_counter()
        try:
            zero_reason = self._zero_score_reason(safe_payload)
            if zero_reason:
                result = self._zero_score_result(zero_reason)
            elif self.provider == "gigachat":
                result = self.gigachat.analyze(safe_payload)
            else:
                result = self.baseline.analyze(safe_payload)
        except Exception as exc:
            logger.exception("Analyzer provider failed; falling back to baseline", extra={"session_id": session_id})
            result = self.baseline.analyze(safe_payload)
            result.error_message = str(exc)

        latency_ms = round((time.perf_counter() - started) * 1000)
        result.latency_ms = latency_ms
        self._cache[cache_key] = result
        logger.info(
            "Answer analysis completed",
            extra={
                "session_id": session_id,
                "provider": result.provider,
                "latency_ms": latency_ms,
                "overall_score": result.overall_score,
            },
        )
        return result

    def _limit_text(self, value: str | None) -> str | None:
        if value is None:
            return None
        return value[: self.max_answer_chars]

    def _cache_key(self, payload: AnswerAnalysisInput) -> str:
        raw = "|".join(
            [
                payload.question_title,
                payload.question_description,
                payload.answer_text or "",
                payload.transcript or "",
                str(payload.has_audio),
            ]
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _zero_score_reason(self, payload: AnswerAnalysisInput) -> str | None:
        answer = (payload.transcript or payload.answer_text or "").strip()
        if not answer:
            return "Empty answer."

        words = re.findall(r"[A-Za-zА-Яа-я0-9]+", answer.lower())
        if len(words) < 4:
            return "Answer is too short to evaluate."

        unique_ratio = len(set(words)) / len(words)
        filler_words = {"bla", "blah", "test", "asdf", "qwerty", "empty", "nothing"}
        filler_count = sum(1 for word in words if word in filler_words)
        if filler_count / len(words) >= 0.5:
            return "Answer looks like placeholder text."

        if len(words) >= 3 and unique_ratio <= 0.35:
            return "Answer is mostly repeated words."

        meaningful_chars = re.findall(r"[A-Za-zА-Яа-я]", answer)
        if len(meaningful_chars) < 12:
            return "Answer has too little meaningful text."

        return None

    def _zero_score_result(self, reason: str) -> AnswerAnalysisResult:
        return AnswerAnalysisResult(
            overall_score=0,
            scores_by_category={
                "structure": 0.0,
                "relevance": 0.0,
                "specificity": 0.0,
                "confidence": 0.0,
                "completeness": 0.0,
            },
            strengths=["No scorable answer was provided"],
            to_improve=[
                "Provide a real answer that addresses the question",
                "Use a clear situation, action, and result",
                "Add concrete details instead of placeholder text",
            ],
            quick_tips=[
                "Write at least a few complete sentences",
                "Answer the exact question",
                "Include one specific example or result",
            ],
            ideal_answer_example=(
                "A strong answer should describe the situation, explain what you did, "
                "and finish with a concrete outcome or lesson."
            ),
            explanation=reason,
            provider="baseline",
            rubric_version=RUBRIC_VERSION,
            error_message=reason,
        )

analyzer_service = AnalyzerService()
