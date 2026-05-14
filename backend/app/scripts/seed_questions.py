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

QUESTION_BANK = {
    "technical": {
        "easy": [
            ("Explain HTTP status code groups", "Describe 2xx, 3xx, 4xx, and 5xx responses and when you would use them."),
            ("What is an index in a database?", "Explain how indexes speed up reads and what trade-offs they introduce."),
            ("Explain authentication vs authorization", "Compare identity verification with permission checks using practical examples."),
            ("What is dependency injection?", "Explain how dependency injection improves testability and separation of concerns."),
            ("Explain synchronous vs asynchronous code", "Compare blocking execution with async flows and mention common pitfalls."),
        ],
        "medium": [
            ("Design a rate limiter", "Cover algorithms, distributed counters, storage, and edge cases."),
            ("Explain optimistic and pessimistic locking", "Compare both approaches and describe when each is useful."),
            ("Debug a slow API endpoint", "Walk through metrics, logs, database checks, profiling, and remediation."),
            ("Design idempotent payment requests", "Cover idempotency keys, retries, duplicate detection, and consistency."),
            ("Explain message queues", "Discuss producers, consumers, retries, dead-letter queues, and delivery guarantees."),
        ],
        "hard": [
            ("Design a distributed cache invalidation strategy", "Cover consistency, TTLs, write-through/write-back, and stampede protection."),
            ("Explain CAP theorem trade-offs", "Discuss consistency, availability, partition tolerance, and practical system choices."),
            ("Design a multi-tenant SaaS data model", "Compare shared tables, schemas, databases, isolation, and migration concerns."),
            ("Investigate production memory leaks", "Describe observability, heap analysis, rollout strategy, and prevention."),
            ("Design exactly-once-like processing", "Discuss idempotency, transactional outbox, deduplication, and failure modes."),
        ],
    },
    "behavioral": {
        "easy": [
            ("Tell me about your favorite project", "Explain your role, the problem, the outcome, and why it mattered."),
            ("Describe your communication style", "Share how you adapt to teammates, stakeholders, and difficult situations."),
            ("Tell me about receiving feedback", "Explain the feedback, your reaction, what changed, and the result."),
            ("Describe how you learn a new topic", "Give a concrete learning process and an example of applying it."),
            ("Tell me about helping a teammate", "Share context, your contribution, and the measurable outcome."),
        ],
        "medium": [
            ("Tell me about a missed deadline", "Explain the root cause, communication, recovery plan, and prevention."),
            ("Describe a disagreement with a senior engineer", "Focus on evidence, collaboration, decision-making, and follow-through."),
            ("Tell me about prioritizing competing work", "Explain criteria, trade-offs, stakeholder alignment, and final impact."),
            ("Describe mentoring someone", "Share the person's goal, your approach, and the observable growth."),
            ("Tell me about handling ambiguity", "Explain how you reduced uncertainty and moved the project forward."),
        ],
        "hard": [
            ("Tell me about a high-stakes incident", "Cover pressure, ownership, coordination, customer impact, and lessons learned."),
            ("Describe changing a team's technical direction", "Explain influence, evidence, resistance, and measurable results."),
            ("Tell me about giving difficult feedback", "Share how you kept it respectful, specific, and useful."),
            ("Describe a time you challenged product scope", "Cover user impact, trade-offs, negotiation, and outcome."),
            ("Tell me about rebuilding trust", "Explain what broke, what you did consistently, and how trust was restored."),
        ],
    },
    "system-design": {
        "easy": [
            ("Design a file upload service", "Cover upload flow, metadata, storage, validation, and basic security."),
            ("Design a todo application backend", "Describe entities, endpoints, persistence, and simple scalability."),
            ("Design a user profile service", "Cover profile data, privacy, caching, and update flows."),
            ("Design a search autocomplete feature", "Discuss prefix matching, ranking, caching, and latency."),
            ("Design email verification", "Cover token generation, expiry, storage, and retry behavior."),
        ],
        "medium": [
            ("Design a news feed", "Cover fan-out, ranking, pagination, caching, and freshness."),
            ("Design a video processing pipeline", "Discuss upload, queues, transcoding, status tracking, and storage."),
            ("Design a booking system", "Cover availability, concurrency, payment states, and cancellation."),
            ("Design an audit log service", "Discuss immutable events, querying, retention, and access control."),
            ("Design feature flags", "Cover targeting, rollout, caching, consistency, and kill switches."),
        ],
        "hard": [
            ("Design a global notification platform", "Cover channels, preferences, rate limits, fan-out, retries, and observability."),
            ("Design collaborative document editing", "Discuss conflict resolution, ordering, presence, persistence, and offline edits."),
            ("Design a large-scale analytics pipeline", "Cover ingestion, stream processing, storage, aggregation, and backfills."),
            ("Design a fraud detection system", "Discuss event ingestion, model scoring, rules, latency, and investigations."),
            ("Design a multi-region API platform", "Cover routing, replication, failover, data residency, and consistency."),
        ],
    },
    "hr": {
        "easy": [
            ("Walk me through your resume", "Create a concise story connecting experience, achievements, and this role."),
            ("Why are you leaving your current role?", "Answer honestly while staying constructive and future-focused."),
            ("What are your strengths?", "Pick strengths relevant to the role and support them with examples."),
            ("What motivates you at work?", "Connect motivation to impact, learning, collaboration, or ownership."),
            ("What type of team do you prefer?", "Explain your collaboration preferences and flexibility."),
        ],
        "medium": [
            ("Where do you want to grow next?", "Connect growth areas with the role and a practical development plan."),
            ("Why should we hire you?", "Summarize role fit, proof from experience, and expected contribution."),
            ("What is your ideal manager relationship?", "Describe communication, autonomy, feedback, and accountability."),
            ("How do you evaluate a company?", "Discuss product, team, engineering culture, growth, and values."),
            ("How do you handle stress?", "Give practical tactics and an example of staying effective."),
        ],
        "hard": [
            ("Explain a gap or pivot in your career", "Frame the transition clearly and connect it to your current direction."),
            ("Describe your compensation priorities", "Balance salary, growth, team quality, scope, and flexibility."),
            ("What would make you reject an offer?", "Answer professionally with values, role fit, and working conditions."),
            ("How would you onboard in the first 90 days?", "Give a practical plan for learning, relationships, and early impact."),
            ("What risks do you see in this role?", "Show thoughtful evaluation while staying constructive and curious."),
        ],
    },
}

for category, levels in QUESTION_BANK.items():
    for difficulty, items in levels.items():
        for index, (title, description) in enumerate(items, start=1):
            QUESTIONS.append(
                {
                    "id": f"q_{category[:3]}_{difficulty[:3]}_{index}",
                    "category": category,
                    "difficulty": difficulty,
                    "title": title,
                    "description": description,
                }
            )


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
