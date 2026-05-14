from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import logging
from pathlib import Path
import tempfile

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import generate_token
from app.db.session import SessionLocal
from app.services.audio_storage import audio_storage
from app.models.answer import Answer, AnswerAnalysis
from app.models.practice_session import PracticeSession
from app.models.question import Question
from app.models.user import User
from app.repositories import (
    AnswerRepository,
    AuthTokenRepository,
    PracticeSessionRepository,
    QuestionRepository,
    UserRepository,
)
from ml import AnswerAnalysisInput
from ml.service import AnalyzerService
from ml.transcription import FasterWhisperTranscriber

logger = logging.getLogger("interviewiq.store")
analyzer_service = AnalyzerService(
    provider=settings.analyzer_provider,
    gigachat_credentials=settings.gigachat_credentials,
    gigachat_model=settings.gigachat_model,
    gigachat_scope=settings.gigachat_scope,
    gigachat_verify_ssl_certs=settings.gigachat_verify_ssl_certs,
    analyzer_timeout_sec=settings.analyzer_timeout_sec,
    max_answer_chars=settings.max_answer_chars,
)
transcriber = FasterWhisperTranscriber(
    model_size=settings.whisper_model_size,
    device=settings.whisper_device,
    compute_type=settings.whisper_compute_type,
)

def iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None

def user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "password": user.password,
        "target_role": user.target_role,
        "experience_level": user.experience_level,
        "created_at": iso(user.created_at),
        "updated_at": iso(user.updated_at),
    }

def onboarding_to_dict(user: User) -> dict:
    return {
        "role": user.target_role,
        "experience_level": user.experience_level,
        "updated_at": iso(user.onboarding_updated_at or user.updated_at),
    }

def question_to_dict(question: Question | None) -> dict | None:
    if question is None:
        return None
    return {
        "id": question.id,
        "category": question.category,
        "difficulty": question.difficulty,
        "target_role": question.target_role,
        "title": question.title,
        "description": question.description,
    }

def session_to_dict(session: PracticeSession) -> dict:
    return {
        "id": session.id,
        "user_id": session.user_id,
        "category": session.category,
        "difficulty": session.difficulty,
        "time_limit_sec": session.time_limit_sec,
        "question_count": session.question_count,
        "status": session.status,
        "question_ids": [item.question_id for item in session.questions],
        "current_question_index": session.current_question_index,
        "answer_ids": [answer.id for answer in session.answers],
        "created_at": iso(session.created_at),
        "started_at": iso(session.started_at),
        "finished_at": iso(session.finished_at),
    }

def answer_to_dict(answer: Answer) -> dict:
    return {
        "id": answer.id,
        "session_id": answer.session_id,
        "question_id": answer.question_id,
        "answer_text": answer.answer_text,
        "transcript": answer.transcript,
        "audio_url": answer.audio_url,
        "audio_id": answer.audio_id,
        "status": answer.status,
        "created_at": iso(answer.created_at),
    }

def analysis_to_dict(analysis: AnswerAnalysis) -> dict:
    return {
        "answer_id": analysis.answer_id,
        "overall_score": analysis.overall_score,
        "scores_by_category": analysis.scores_by_category,
        "strengths": analysis.strengths,
        "to_improve": analysis.to_improve,
        "quick_tips": analysis.quick_tips,
        "ideal_answer_example": analysis.ideal_answer_example,
        "explanation": analysis.explanation,
        "provider": analysis.provider,
        "rubric_version": analysis.rubric_version,
        "raw_response": analysis.raw_response,
        "error_message": analysis.error_message,
        "latency_ms": analysis.latency_ms,
        "transcript": analysis.answer.transcript if analysis.answer else None,
    }

def average(values: list[int]) -> int:
    return int(sum(values) / len(values)) if values else 0

def session_average(answers: list[Answer]) -> int:
    return average([answer.analysis.overall_score for answer in answers if answer.analysis])

def normalize_category_score(value: int | float) -> int:
    numeric = float(value)
    if numeric <= 1:
        numeric *= 100
    return int(max(0, min(100, round(numeric))))

def normalize_target_role(role: str | None) -> str | None:
    if not role:
        return None

    aliases = {
        "backend engineer": "Software Engineer",
        "data science": "Data Scientist",
        "ml engineer": "Data Scientist",
        "product analyst": "Product Manager",
    }
    normalized = " ".join(role.strip().split())
    return aliases.get(normalized.lower(), normalized)

class DatabaseStore:
    @contextmanager
    def db(self) -> Iterator[Session]:
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_user(self, full_name: str, email: str, password: str) -> dict:
        with self.db() as db:
            users = UserRepository(db)
            if users.get_by_email(email):
                raise ValueError("Email already exists")
            try:
                user = users.create(full_name=full_name, email=email, password=password)
                db.flush()
                return user_to_dict(user)
            except IntegrityError as exc:
                raise ValueError("Email already exists") from exc

    def authenticate(self, email: str, password: str) -> dict | None:
        with self.db() as db:
            user = UserRepository(db).get_by_email(email)
            if user is None or user.password != password:
                return None
            return user_to_dict(user)

    def issue_tokens(self, user_id: str) -> dict[str, str]:
        with self.db() as db:
            tokens = AuthTokenRepository(db)
            access_token = generate_token("acc")
            refresh_token = generate_token("ref")
            tokens.create(user_id=user_id, token=access_token, token_type="access")
            tokens.create(user_id=user_id, token=refresh_token, token_type="refresh")
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }

    def get_user_by_token(self, token: str) -> dict | None:
        with self.db() as db:
            user = AuthTokenRepository(db).get_user_by_token(token)
            return user_to_dict(user) if user else None

    def update_onboarding(self, user_id: str, role: str, experience_level: str) -> dict:
        with self.db() as db:
            user = UserRepository(db).update_onboarding(
                user_id=user_id,
                role=role,
                experience_level=experience_level,
            )
            return onboarding_to_dict(user)

    def get_onboarding(self, user_id: str) -> dict:
        with self.db() as db:
            user = UserRepository(db).get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")
            return onboarding_to_dict(user)

    def update_profile(
        self,
        user_id: str,
        full_name: str | None,
        target_role: str | None,
        experience_level: str | None,
    ) -> dict:
        with self.db() as db:
            user = UserRepository(db).update_profile(
                user_id=user_id,
                full_name=full_name,
                target_role=target_role,
                experience_level=experience_level,
            )
            return user_to_dict(user)

    def filter_questions(
        self,
        category: str | None = None,
        difficulty: str | None = None,
        target_role: str | None = None,
        limit: int = 10,
    ) -> list[dict]:
        with self.db() as db:
            questions = QuestionRepository(db).list_questions(
                category=category,
                difficulty=difficulty,
                target_role=target_role,
                limit=limit,
            )
            return [question_to_dict(question) for question in questions if question is not None]

    def create_session(
        self,
        user_id: str,
        category: str,
        difficulty: str,
        time_limit_sec: int,
        question_count: int,
    ) -> dict:
        with self.db() as db:
            user = UserRepository(db).get_by_id(user_id)
            target_role = normalize_target_role(user.target_role if user else None)
            question_repo = QuestionRepository(db)
            candidates = question_repo.list_questions(
                category=category,
                difficulty=difficulty,
                target_role=target_role,
                limit=100,
            )
            if not candidates:
                candidates = question_repo.list_questions(
                    category=category,
                    target_role=target_role,
                    limit=100,
                )
            if not candidates:
                candidates = question_repo.list_questions(category=category, difficulty=difficulty, limit=100)
            if not candidates:
                candidates = question_repo.list_questions(category=category, limit=100)
            if not candidates:
                candidates = question_repo.list_questions(limit=100)
            if not candidates:
                raise ValueError("No questions available")

            selected = candidates[: max(1, min(question_count, len(candidates)))]
            session = PracticeSessionRepository(db).create(
                user_id=user_id,
                category=category,
                difficulty=difficulty,
                time_limit_sec=time_limit_sec,
                questions=selected,
            )
            return session_to_dict(session)

    def get_session(self, user_id: str, session_id: str) -> dict | None:
        with self.db() as db:
            session = PracticeSessionRepository(db).get_for_user(user_id=user_id, session_id=session_id)
            return session_to_dict(session) if session else None

    def start_session(self, session: dict) -> dict:
        with self.db() as db:
            repo = PracticeSessionRepository(db)
            db_session = repo.get_for_user(user_id=session["user_id"], session_id=session["id"])
            if db_session is None:
                raise ValueError("Session not found")
            return session_to_dict(repo.start(db_session))

    def finish_session(self, session: dict) -> dict:
        with self.db() as db:
            repo = PracticeSessionRepository(db)
            db_session = repo.get_for_user(user_id=session["user_id"], session_id=session["id"])
            if db_session is None:
                raise ValueError("Session not found")
            return session_to_dict(repo.finish(db_session))

    def get_question_by_id(self, question_id: str) -> dict | None:
        with self.db() as db:
            question = QuestionRepository(db).get(question_id)
            return question_to_dict(question)

    def get_current_question(self, session: dict) -> dict | None:
        with self.db() as db:
            db_session = PracticeSessionRepository(db).get_for_user(
                user_id=session["user_id"],
                session_id=session["id"],
            )
            if db_session is None:
                return None
            question = PracticeSessionRepository(db).current_question(db_session)
            return question_to_dict(question)

    def next_question(self, session: dict) -> dict | None:
        with self.db() as db:
            repo = PracticeSessionRepository(db)
            db_session = repo.get_for_user(user_id=session["user_id"], session_id=session["id"])
            if db_session is None:
                return None
            question = repo.move_next(db_session)
            session.update(session_to_dict(db_session))
            return question_to_dict(question)

    def submit_answer(
        self,
        session: dict,
        question_id: str,
        answer_text: str | None,
        audio_url: str | None,
        audio_id: str | None,
    ) -> tuple[dict, dict]:
        transcript = None
        clean_answer_text = (answer_text or "").strip() or None
        if clean_answer_text is None and audio_id:
            transcript = self._transcribe_audio(audio_id=audio_id, session_id=session["id"])

        with self.db() as db:
            question = QuestionRepository(db).get(question_id)
            if question is None:
                raise ValueError("Question not found")

            payload = AnswerAnalysisInput(
                answer_text=clean_answer_text,
                question_title=question.title,
                question_description=question.description,
                category=question.category,
                difficulty=question.difficulty,
                has_audio=bool(audio_url or audio_id),
                audio_url=audio_url,
                transcript=transcript,
            )
            result = analyzer_service.analyze(payload, session_id=session["id"])
            analysis_data = result.model_dump(
                include={
                    "overall_score",
                    "scores_by_category",
                    "strengths",
                    "to_improve",
                    "quick_tips",
                    "ideal_answer_example",
                    "explanation",
                    "provider",
                    "rubric_version",
                    "raw_response",
                    "error_message",
                    "latency_ms",
                }
            )
            logger.info(
                "Persisting answer analysis",
                extra={
                    "session_id": session["id"],
                    "provider": result.provider,
                    "score": result.overall_score,
                },
            )
            answer, analysis = AnswerRepository(db).create_with_analysis(
                session_id=session["id"],
                question_id=question_id,
                answer_text=clean_answer_text,
                transcript=transcript,
                audio_url=audio_url,
                audio_id=audio_id,
                analysis_data=analysis_data,
            )
            return answer_to_dict(answer), analysis_to_dict(analysis)

    def _transcribe_audio(self, audio_id: str, session_id: str) -> str | None:
        suffix = Path(audio_id).suffix or ".m4a"
        with tempfile.TemporaryDirectory(prefix="interviewiq-audio-") as tmp_dir:
            audio_path = Path(tmp_dir) / f"answer{suffix}"
            try:
                audio_storage.download_audio(audio_id=audio_id, destination=audio_path)
                result = transcriber.transcribe(audio_path)
                logger.info(
                    "Audio transcription completed",
                    extra={
                        "session_id": session_id,
                        "language": result.language,
                        "language_probability": result.language_probability,
                    },
                )
                return result.text or None
            except Exception as exc:
                logger.exception("Audio transcription failed", extra={"session_id": session_id})
                return None

    def get_analysis(self, session: dict, answer_id: str) -> dict | None:
        if answer_id not in session["answer_ids"]:
            return None
        with self.db() as db:
            analysis = AnswerRepository(db).get_analysis(answer_id)
            return analysis_to_dict(analysis) if analysis else None

    def get_session_results(self, session: dict) -> dict:
        with self.db() as db:
            answers = AnswerRepository(db).list_for_session(session["id"])
            scores = [answer.analysis.overall_score for answer in answers if answer.analysis]
            avg_score = int(sum(scores) / len(scores)) if scores else 0
            question_results = [
                {
                    "answer_id": answer.id,
                    "question_id": answer.question_id,
                    "question_title": answer.question.title if answer.question else "Unknown question",
                    "score": answer.analysis.overall_score if answer.analysis else 0,
                }
                for answer in answers
            ]

            return {
                "session_id": session["id"],
                "status": session["status"],
                "average_score": avg_score,
                "questions_answered": len(question_results),
                "question_results": question_results,
                "finished_at": session["finished_at"],
            }

    def analytics_overview(self, user_id: str) -> dict:
        with self.db() as db:
            finished = PracticeSessionRepository(db).list_finished_for_user(user_id)
            if not finished:
                return {"readiness_score": 0, "average_score": 0, "trend_percent": 0}

            session_scores = []
            recent_answer_scores = []
            for session in finished:
                answers = AnswerRepository(db).list_for_session(session.id)
                session_scores.append(session_average(answers))
                for answer in answers:
                    if answer.analysis:
                        recent_answer_scores.append(answer.analysis.overall_score)

            avg = average(recent_answer_scores[:20])
            trend = session_scores[0] - session_scores[1] if len(session_scores) >= 2 else 0
            return {"readiness_score": avg, "average_score": avg, "trend_percent": trend}

    def analytics_skills(self, user_id: str) -> list[dict]:
        with self.db() as db:
            finished = PracticeSessionRepository(db).list_finished_for_user(user_id)
            buckets: dict[str, list[int]] = {}
            previous_buckets: dict[str, list[int]] = {}

            for index, session in enumerate(finished):
                answers = AnswerRepository(db).list_for_session(session.id)
                for answer in answers:
                    if not answer.analysis:
                        continue
                    for name, raw_score in answer.analysis.scores_by_category.items():
                        label = str(name).replace("_", " ").title()
                        score = normalize_category_score(raw_score)
                        buckets.setdefault(label, []).append(score)
                        if index > 0:
                            previous_buckets.setdefault(label, []).append(score)

            if not buckets and not previous_buckets:
                return []

            skill_names = sorted(set(buckets) | set(previous_buckets))
            return [
                {
                    "name": name,
                    "score": average(buckets.get(name, [])),
                    "change": average(buckets.get(name, [])) - average(previous_buckets.get(name, [])),
                }
                for name in skill_names
            ]

    def analytics_weekly_progress(self, user_id: str) -> list[dict]:
        today = datetime.now(timezone.utc).date()
        week_start = today - timedelta(days=today.weekday())
        points = [
            {"day": (week_start + timedelta(days=offset)).strftime("%a"), "score": 0}
            for offset in range(7)
        ]

        with self.db() as db:
            finished = PracticeSessionRepository(db).list_finished_for_user(user_id)
            scores_by_day: dict[int, list[int]] = {offset: [] for offset in range(7)}

            for session in finished:
                if not session.finished_at:
                    continue
                finished_at = session.finished_at
                if finished_at.tzinfo is None:
                    finished_at = finished_at.replace(tzinfo=timezone.utc)
                session_date = finished_at.date()
                if session_date < week_start or session_date > today:
                    continue
                answers = AnswerRepository(db).list_for_session(session.id)
                scores_by_day[(session_date - week_start).days].append(session_average(answers))

            for offset, scores in scores_by_day.items():
                points[offset]["score"] = average(scores)

        return points

    def analytics_sessions(self, user_id: str) -> list[dict]:
        with self.db() as db:
            finished = PracticeSessionRepository(db).list_finished_for_user(user_id)
            items = []
            for session in finished:
                answers = AnswerRepository(db).list_for_session(session.id)
                score = session_average(answers)
                if session.started_at and session.finished_at:
                    duration_min = max(1, int((session.finished_at - session.started_at).total_seconds() / 60))
                else:
                    duration_min = max(1, int((session.time_limit_sec * session.question_count) / 60))
                items.append(
                    {
                        "session_id": session.id,
                        "category": session.category,
                        "score": score,
                        "completed_at": iso(session.finished_at),
                        "questions_count": session.question_count,
                        "duration_min": duration_min,
                    }
                )
            return items

    def dashboard_home(self, user_id: str) -> dict:
        overview = self.analytics_overview(user_id)
        history = self.analytics_sessions(user_id)

        with self.db() as db:
            latest = PracticeSessionRepository(db).latest_active_for_user(user_id)
            resume = None
            if latest:
                resume = {
                    "session_id": latest.id,
                    "question_index": latest.current_question_index + 1,
                    "total_questions": latest.question_count,
                }

        return {
            "progress_card": {
                "value": overview["readiness_score"],
                "trend": f"{overview['trend_percent']:+d}% this week",
                "subtitle": "Keep practicing to improve consistency",
            },
            "areas_to_improve": [
                {"skill": item["name"], "score": item["score"]}
                for item in sorted(self.analytics_skills(user_id), key=lambda item: item["score"])[:3]
            ],
            "recent_sessions": history[:3],
            "resume_session": resume,
        }

store = DatabaseStore()
