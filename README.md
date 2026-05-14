# InterviewIQ

Mobile interview practice app: NativeScript + Vue frontend, FastAPI backend, PostgreSQL storage, optional GigaChat analysis, FCM reminders, and MinIO/local audio storage.

## Requirements

- Node.js 20+
- NativeScript CLI
- Python 3.11+
- PostgreSQL
- Android emulator or real Android device

## Backend

1. Create `backend/api.env` from your local secrets template. Keep real keys out of git.
2. Create a fresh PostgreSQL database and set the database URL in `backend/api.env`.
3. Install dependencies:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

4. Apply migrations and seed questions:

```bash
alembic upgrade head
python -m app.scripts.seed_questions
```

5. Start API:

```bash
uvicorn app.main:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`

## Frontend

Install packages from the repo root:

```bash
npm ci
```

Run on Android:

```bash
ns run android
```

Android emulator uses `http://10.0.2.2:8000/api/v1` by default. iOS/local uses `http://127.0.0.1:8000/api/v1`.

## Clean Install Check

1. Drop/create a clean PostgreSQL database.
2. Run `alembic upgrade head`.
3. Run `python -m app.scripts.seed_questions`.
4. Start backend with `uvicorn app.main:app --reload`.
5. Run mobile app with `npm ci` then `ns run android`.
6. Complete the flow: sign up, onboarding, start practice, answer questions, finish session, open Home, Analytics, Profile.

## Demo Script

1. Sign in or create a demo user and show onboarding role/level.
2. Start a practice session, answer one question with text or audio.
3. Open the result screen and show score, strengths, improvements, and category breakdown.
4. Finish the session and show Analytics: weekly progress, skills breakdown, recent sessions.
5. Return to Home/Profile and show API-backed progress and profile stats.

## Demo Fallbacks

- If FCM push does not arrive, show the `/notifications/test-reminder` Postman response.
- If GigaChat is unavailable, use the baseline analyzer fallback and mention provider fallback in the response.
- If emulator microphone is unstable, submit a text answer, use pre-recorded audio, or test on a real phone.

## Notes

- PostgreSQL can easily handle thousands of interview questions for this project. Keep indexes on `category` and `difficulty` and paginate API responses if the dataset grows very large.
- To import the full HR dataset from `dataset/hr_interview_questions_dataset.json`, run:

```bash
cd backend
python -m app.scripts.seed_dataset_questions
```

  For a quick smoke test, import a small slice first:

```bash
python -m app.scripts.seed_dataset_questions --limit 1000
```

  By default, HR dataset topics are mapped to practice categories:
  `adaptability`, `career-goals`, `conflict-resolution`, `culture-fit`, `leadership`,
  `motivation`, `team-collaboration`, and `work-style`. Dataset roles are stored in
  `questions.target_role`, so run `alembic upgrade head` before importing.

  If you have another dataset with the same JSON shape, choose the application category explicitly:

```bash
python -m app.scripts.seed_dataset_questions --path ..\dataset\technical_questions.json --target-category technical
python -m app.scripts.seed_dataset_questions --path ..\dataset\behavioral_questions.json --target-category behavioral
python -m app.scripts.seed_dataset_questions --path ..\dataset\system_design_questions.json --target-category system-design
```

- Dark Mode is currently only a preference toggle. Full theme support needs a separate pass over global colors and component styles.
