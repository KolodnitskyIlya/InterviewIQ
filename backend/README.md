# InterviewIQ Backend (MVP)

FastAPI scaffold for InterviewIQ mobile app.

## Quick start

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API base URL: `http://127.0.0.1:8000/api/v1`
Swagger: `http://127.0.0.1:8000/docs`

## Notes

- Storage is in-memory only (for MVP scaffold).
- Restarting server resets users/sessions/answers.
- Replace `services/store.py` with DB-backed repositories later.
