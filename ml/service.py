import hashlib
import logging
import time
from ml.base import AnswerAnalysisInput, AnswerAnalysisResult
from ml.baseline import BaselineAnalyzer
from ml.gigachat import DeepSeekAnalyzer
from ml.llm import LLMAnalyzer

logger = logging.getLogger("interviewiq.analyzer")

class AnalyzerService:
    def __init__(
        self,
        provider: str = "baseline",
        openai_api_key: str = "",
        openai_model: str = "gpt-4.1-mini",
        deepseek_api_key: str = "",
        deepseek_model: str = "deepseek-v4-flash",
        deepseek_base_url: str = "https://api.deepseek.com",
        llm_timeout_sec: int = 20,
        max_answer_chars: int = 6000,
    ) -> None:
        self.provider = provider
        self.max_answer_chars = max_answer_chars
        self.baseline = BaselineAnalyzer()
        self.llm = LLMAnalyzer(
            api_key=openai_api_key,
            model=openai_model,
            timeout_sec=llm_timeout_sec,
        )
        self.deepseek = DeepSeekAnalyzer(
            api_key=deepseek_api_key,
            model=deepseek_model,
            base_url=deepseek_base_url,
            timeout_sec=llm_timeout_sec,
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
            has_text = bool((safe_payload.answer_text or safe_payload.transcript or "").strip())
            if not has_text and not safe_payload.has_audio:
                result = self.baseline.analyze(safe_payload)
                result.error_message = "Empty answer without audio was scored by baseline only."
            elif self.provider == "deepseek":
                result = self.deepseek.analyze(safe_payload)
            elif self.provider == "llm":
                result = self.llm.analyze(safe_payload)
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

analyzer_service = AnalyzerService()
