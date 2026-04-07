from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from app.core.security import generate_token

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class InMemoryStore:
    def __init__(self) -> None:
        self.users: dict[str, dict[str, Any]] = {}
        self.users_by_email: dict[str, str] = {}
        self.access_tokens: dict[str, str] = {}
        self.refresh_tokens: dict[str, str] = {}
        self.onboarding: dict[str, dict[str, Any]] = {}
        self.sessions: dict[str, dict[str, Any]] = {}
        self.answers: dict[str, dict[str, Any]] = {}
        self.analyses: dict[str, dict[str, Any]] = {}
        self.questions: list[dict[str, Any]] = self._seed_questions()

    def _seed_questions(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "q_1",
                "category": "technical",
                "difficulty": "easy",
                "title": "Explain REST and GraphQL differences",
                "description": "Compare APIs by flexibility, payload size, and versioning approach.",
            },
            {
                "id": "q_2",
                "category": "technical",
                "difficulty": "medium",
                "title": "Design a URL shortener",
                "description": "Describe storage model, collision handling, and scaling strategy.",
            },
            {
                "id": "q_3",
                "category": "behavioral",
                "difficulty": "easy",
                "title": "Tell me about a team conflict",
                "description": "Share context, your actions, and the final outcome.",
            },
            {
                "id": "q_4",
                "category": "behavioral",
                "difficulty": "hard",
                "title": "Describe a major failure and recovery",
                "description": "Focus on responsibility, lessons learned, and measurable changes.",
            },
            {
                "id": "q_5",
                "category": "system-design",
                "difficulty": "medium",
                "title": "Design a notification service",
                "description": "Cover architecture, retries, delivery guarantees, and monitoring.",
            },
            {
                "id": "q_6",
                "category": "hr",
                "difficulty": "easy",
                "title": "Why do you want this role?",
                "description": "Connect your background with role expectations and growth goals.",
            },
        ]

    def create_user(self, full_name: str, email: str, password: str) -> dict[str, Any]:
        normalized_email = email.strip().lower()
        if normalized_email in self.users_by_email:
            raise ValueError("Email already exists")

        user_id = f"u_{uuid4().hex[:12]}"
        now = now_iso()
        user = {
            "id": user_id,
            "full_name": full_name.strip(),
            "email": normalized_email,
            "password": password,
            "target_role": None,
            "experience_level": None,
            "created_at": now,
            "updated_at": now,
        }
        self.users[user_id] = user
        self.users_by_email[normalized_email] = user_id
        self.onboarding[user_id] = {
            "role": None,
            "experience_level": None,
            "updated_at": now,
        }
        return user

    def authenticate(self, email: str, password: str) -> dict[str, Any] | None:
        normalized_email = email.strip().lower()
        user_id = self.users_by_email.get(normalized_email)
        if not user_id:
            return None
        user = self.users[user_id]
        if user["password"] != password:
            return None
        return user

    def issue_tokens(self, user_id: str) -> dict[str, str]:
        access_token = generate_token("acc")
        refresh_token = generate_token("ref")
        self.access_tokens[access_token] = user_id
        self.refresh_tokens[refresh_token] = user_id
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def get_user_by_token(self, token: str) -> dict[str, Any] | None:
        user_id = self.access_tokens.get(token)
        if not user_id:
            return None
        return self.users.get(user_id)

    def update_onboarding(self, user_id: str, role: str, experience_level: str) -> dict[str, Any]:
        state = {
            "role": role,
            "experience_level": experience_level,
            "updated_at": now_iso(),
        }
        self.onboarding[user_id] = state
        user = self.users[user_id]
        user["target_role"] = role
        user["experience_level"] = experience_level
        user["updated_at"] = state["updated_at"]
        return state

    def get_onboarding(self, user_id: str) -> dict[str, Any]:
        return self.onboarding[user_id]

    def update_profile(
        self,
        user_id: str,
        full_name: str | None,
        target_role: str | None,
        experience_level: str | None,
    ) -> dict[str, Any]:
        user = self.users[user_id]
        if full_name is not None:
            user["full_name"] = full_name.strip()
        if target_role is not None:
            user["target_role"] = target_role
        if experience_level is not None:
            user["experience_level"] = experience_level
        user["updated_at"] = now_iso()
        return user

    def filter_questions(
        self,
        category: str | None = None,
        difficulty: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        items = self.questions
        if category:
            items = [q for q in items if q["category"] == category]
        if difficulty:
            items = [q for q in items if q["difficulty"] == difficulty]
        return items[:limit]

    def create_session(
        self,
        user_id: str,
        category: str,
        difficulty: str,
        time_limit_sec: int,
        question_count: int,
    ) -> dict[str, Any]:
        candidates = self.filter_questions(category=category, difficulty=difficulty, limit=50)
        if not candidates:
            candidates = self.filter_questions(limit=50)

        question_count = max(1, min(question_count, len(candidates)))
        selected = candidates[:question_count]

        session_id = f"s_{uuid4().hex[:12]}"
        session = {
            "id": session_id,
            "user_id": user_id,
            "category": category,
            "difficulty": difficulty,
            "time_limit_sec": time_limit_sec,
            "question_count": question_count,
            "status": "created",
            "question_ids": [q["id"] for q in selected],
            "current_question_index": 0,
            "answer_ids": [],
            "created_at": now_iso(),
            "started_at": None,
            "finished_at": None,
        }
        self.sessions[session_id] = session
        return session

    def get_session(self, user_id: str, session_id: str) -> dict[str, Any] | None:
        session = self.sessions.get(session_id)
        if not session:
            return None
        if session["user_id"] != user_id:
            return None
        return session

    def start_session(self, session: dict[str, Any]) -> dict[str, Any]:
        if session["status"] == "created":
            session["status"] = "in_progress"
            session["started_at"] = now_iso()
        return session

    def finish_session(self, session: dict[str, Any]) -> dict[str, Any]:
        session["status"] = "finished"
        if not session["started_at"]:
            session["started_at"] = now_iso()
        session["finished_at"] = now_iso()
        return session

    def get_question_by_id(self, question_id: str) -> dict[str, Any] | None:
        for question in self.questions:
            if question["id"] == question_id:
                return question
        return None

    def get_current_question(self, session: dict[str, Any]) -> dict[str, Any] | None:
        index = session["current_question_index"]
        if index >= len(session["question_ids"]):
            return None
        question_id = session["question_ids"][index]
        return self.get_question_by_id(question_id)

    def next_question(self, session: dict[str, Any]) -> dict[str, Any] | None:
        if session["current_question_index"] + 1 >= len(session["question_ids"]):
            return None
        session["current_question_index"] += 1
        return self.get_current_question(session)

    def submit_answer(
        self,
        session: dict[str, Any],
        question_id: str,
        answer_text: str | None,
        audio_url: str | None,
        audio_id: str | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        answer_id = f"a_{uuid4().hex[:12]}"
        text_len = len((answer_text or "").strip())
        base_score = min(100, 35 + text_len // 4)
        has_numbers = any(ch.isdigit() for ch in (answer_text or ""))
        specificity = min(1.0, 0.45 + (0.15 if has_numbers else 0.0) + min(0.3, text_len / 500))

        analysis = {
            "answer_id": answer_id,
            "overall_score": int(base_score),
            "scores_by_category": {
                "completeness": round(min(1.0, 0.35 + text_len / 350), 2),
                "specificity": round(specificity, 2),
                "structure": 0.62,
                "confidence": 0.71,
                "relevance": 0.8,
            },
            "strengths": [
                "Relevant answer direction",
                "Clear core idea",
            ],
            "to_improve": [
                "Add more measurable details",
                "Describe your personal contribution",
                "Use STAR structure",
            ],
            "quick_tips": [
                "Speak for 60-120 seconds",
                "Add one concrete metric",
                "Finish with impact",
            ],
            "ideal_answer_example": "I led a migration of three legacy services to a new API gateway. We cut average response time by 38% and reduced incidents by 42% over two months.",
        }

        answer = {
            "id": answer_id,
            "session_id": session["id"],
            "question_id": question_id,
            "answer_text": answer_text,
            "audio_url": audio_url,
            "audio_id": audio_id,
            "status": "processed",
            "created_at": now_iso(),
        }
        self.answers[answer_id] = answer
        self.analyses[answer_id] = analysis
        session["answer_ids"].append(answer_id)

        return answer, analysis

    def get_analysis(self, session: dict[str, Any], answer_id: str) -> dict[str, Any] | None:
        if answer_id not in session["answer_ids"]:
            return None
        return self.analyses.get(answer_id)

    def get_session_results(self, session: dict[str, Any]) -> dict[str, Any]:
        analyses = [self.analyses[aid] for aid in session["answer_ids"] if aid in self.analyses]
        avg_score = int(sum(a["overall_score"] for a in analyses) / len(analyses)) if analyses else 0

        question_results = []
        for answer_id in session["answer_ids"]:
            answer = self.answers.get(answer_id)
            if not answer:
                continue
            analysis = self.analyses.get(answer_id)
            question = self.get_question_by_id(answer["question_id"])
            question_results.append(
                {
                    "answer_id": answer_id,
                    "question_id": answer["question_id"],
                    "question_title": question["title"] if question else "Unknown question",
                    "score": analysis["overall_score"] if analysis else 0,
                }
            )

        return {
            "session_id": session["id"],
            "status": session["status"],
            "average_score": avg_score,
            "questions_answered": len(question_results),
            "question_results": question_results,
            "finished_at": session["finished_at"],
        }

    def analytics_overview(self, user_id: str) -> dict[str, Any]:
        finished = [s for s in self.sessions.values() if s["user_id"] == user_id and s["status"] == "finished"]
        if not finished:
            return {
                "readiness_score": 0,
                "average_score": 0,
                "trend_percent": 0,
            }

        scores = [self.get_session_results(s)["average_score"] for s in finished]
        avg = int(sum(scores) / len(scores)) if scores else 0
        trend = 0
        if len(scores) >= 2:
            trend = scores[-1] - scores[-2]

        return {
            "readiness_score": avg,
            "average_score": avg,
            "trend_percent": trend,
        }

    def analytics_skills(self, user_id: str) -> list[dict[str, Any]]:
        return [
            {"name": "Technical", "score": 72, "change": 4},
            {"name": "Behavioral", "score": 68, "change": 6},
            {"name": "Structure", "score": 64, "change": 3},
            {"name": "Confidence", "score": 75, "change": 2},
        ]

    def analytics_weekly_progress(self, user_id: str) -> list[dict[str, Any]]:
        return [
            {"day": "Mon", "score": 62},
            {"day": "Tue", "score": 64},
            {"day": "Wed", "score": 67},
            {"day": "Thu", "score": 70},
            {"day": "Fri", "score": 72},
            {"day": "Sat", "score": 74},
            {"day": "Sun", "score": 76},
        ]

    def analytics_sessions(self, user_id: str) -> list[dict[str, Any]]:
        finished = [s for s in self.sessions.values() if s["user_id"] == user_id and s["status"] == "finished"]
        finished.sort(key=lambda item: item["finished_at"] or "", reverse=True)
        items = []
        for session in finished:
            result = self.get_session_results(session)
            items.append(
                {
                    "session_id": session["id"],
                    "category": session["category"],
                    "score": result["average_score"],
                    "completed_at": session["finished_at"],
                    "questions_count": session["question_count"],
                    "duration_min": max(1, int((session["time_limit_sec"] * session["question_count"]) / 60)),
                }
            )
        return items

    def dashboard_home(self, user_id: str) -> dict[str, Any]:
        overview = self.analytics_overview(user_id)
        history = self.analytics_sessions(user_id)
        in_progress = [
            s
            for s in self.sessions.values()
            if s["user_id"] == user_id and s["status"] in {"created", "in_progress"}
        ]

        resume = None
        if in_progress:
            latest = sorted(in_progress, key=lambda item: item["created_at"], reverse=True)[0]
            resume = {
                "session_id": latest["id"],
                "question_index": latest["current_question_index"] + 1,
                "total_questions": latest["question_count"],
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

store = InMemoryStore()
