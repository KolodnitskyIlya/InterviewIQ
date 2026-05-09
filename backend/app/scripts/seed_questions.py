from app.db.session import SessionLocal
from app.repositories.questions import QuestionRepository

QUESTIONS = [
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
    {
        "id": "q_7",
        "category": "technical",
        "difficulty": "hard",
        "title": "Explain database transaction isolation levels",
        "description": "Discuss dirty reads, non-repeatable reads, phantom reads, and trade-offs.",
    },
    {
        "id": "q_8",
        "category": "system-design",
        "difficulty": "hard",
        "title": "Design a real-time chat system",
        "description": "Cover WebSocket connections, message persistence, ordering, and offline delivery.",
    },
    {
        "id": "q_9",
        "category": "behavioral",
        "difficulty": "medium",
        "title": "Tell me about a time you improved a process",
        "description": "Explain the problem, your initiative, measurable result, and what changed long-term.",
    },
    {
        "id": "q_10",
        "category": "hr",
        "difficulty": "medium",
        "title": "What are your salary expectations?",
        "description": "Give a concise answer that balances flexibility, market awareness, and confidence.",
    },
]


def main() -> None:
    db = SessionLocal()
    try:
        added = QuestionRepository(db).upsert_many(QUESTIONS)
        db.commit()
        print(f"Seeded {len(QUESTIONS)} questions ({added} new).")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
