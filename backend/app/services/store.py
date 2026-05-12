from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import generate_token
from app.db.session import SessionLocal
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

logger = logging.getLogger("interviewiq.store")
analyzer_service = AnalyzerService(
    provider=settings.analyzer_provider,
    openai_api_key=settings.openai_api_key,
    openai_model=settings.openai_model,
    deepseek_api_key=settings.deepseek_api_key,
    deepseek_model=settings.deepseek_model,
    deepseek_base_url=settings.deepseek_base_url,
    llm_timeout_sec=settings.llm_timeout_sec,
    max_answer_chars=settings.max_answer_chars,
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
    }

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
        limit: int = 10,
    ) -> list[dict]:
        with self.db() as db:
            questions = QuestionRepository(db).list_questions(category=category, difficulty=difficulty, limit=limit)
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
            question_repo = QuestionRepository(db)
            candidates = question_repo.list_questions(category=category, difficulty=difficulty, limit=50)
            if not candidates:
                candidates = question_repo.list_questions(limit=50)
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
        with self.db() as db:
            question = QuestionRepository(db).get(question_id)
            if question is None:
                raise ValueError("Question not found")

            payload = AnswerAnalysisInput(
                answer_text=answer_text,
                question_title=question.title,
                question_description=question.description,
                category=question.category,
                difficulty=question.difficulty,
                has_audio=bool(audio_url or audio_id),
                audio_url=audio_url,
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
                answer_text=answer_text,
                audio_url=audio_url,
                audio_id=audio_id,
                analysis_data=analysis_data,
            )
            return answer_to_dict(answer), analysis_to_dict(analysis)

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

            scores = []
            for session in finished:
                answers = AnswerRepository(db).list_for_session(session.id)
                answer_scores = [answer.analysis.overall_score for answer in answers if answer.analysis]
                scores.append(int(sum(answer_scores) / len(answer_scores)) if answer_scores else 0)

            avg = int(sum(scores) / len(scores)) if scores else 0
            trend = scores[0] - scores[1] if len(scores) >= 2 else 0
            return {"readiness_score": avg, "average_score": avg, "trend_percent": trend}

    def analytics_skills(self, user_id: str) -> list[dict]:
        return [
            {"name": "Technical", "score": 72, "change": 4},
            {"name": "Behavioral", "score": 68, "change": 6},
            {"name": "Structure", "score": 64, "change": 3},
            {"name": "Confidence", "score": 75, "change": 2},
        ]

    def analytics_weekly_progress(self, user_id: str) -> list[dict]:
        return [
            {"day": "Mon", "score": 62},
            {"day": "Tue", "score": 64},
            {"day": "Wed", "score": 67},
            {"day": "Thu", "score": 70},
            {"day": "Fri", "score": 72},
            {"day": "Sat", "score": 74},
            {"day": "Sun", "score": 76},
        ]

    def analytics_sessions(self, user_id: str) -> list[dict]:
        with self.db() as db:
            finished = PracticeSessionRepository(db).list_finished_for_user(user_id)
            items = []
            for session in finished:
                answers = AnswerRepository(db).list_for_session(session.id)
                answer_scores = [answer.analysis.overall_score for answer in answers if answer.analysis]
                score = int(sum(answer_scores) / len(answer_scores)) if answer_scores else 0
                items.append(
                    {
                        "session_id": session.id,
                        "category": session.category,
                        "score": score,
                        "completed_at": iso(session.finished_at),
                        "questions_count": session.question_count,
                        "duration_min": max(1, int((session.time_limit_sec * session.question_count) / 60)),
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
                {"skill": "Structure", "score": 64},
                {"skill": "Behavioral depth", "score": 68},
                {"skill": "Specificity", "score": 70},
            ],
            "recent_sessions": history[:3],
            "resume_session": resume,
        }

store = DatabaseStore()
