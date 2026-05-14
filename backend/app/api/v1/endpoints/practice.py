from fastapi import APIRouter, Depends, HTTPException, Query
from botocore.exceptions import BotoCoreError, ClientError
from app.core.deps import get_current_user
from app.schemas.answer import (
    AnswerAnalysisResponse,
    AudioUploadRequest,
    AudioUploadResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)
from app.schemas.practice import (
    CreateSessionRequest,
    PracticeConfigResponse,
    SessionResultsResponse,
    SessionStateResponse,
)
from app.schemas.question import SessionQuestionResponse
from app.services.audio_storage import audio_storage
from app.services.store import store

router = APIRouter(tags=["practice"])

def _session_state(session: dict) -> dict:
    return {
        "id": session["id"],
        "status": session["status"],
        "category": session["category"],
        "difficulty": session["difficulty"],
        "time_limit_sec": session["time_limit_sec"],
        "question_count": session["question_count"],
        "current_question_index": session["current_question_index"],
        "created_at": session["created_at"],
        "started_at": session["started_at"],
        "finished_at": session["finished_at"],
    }

@router.get("/practice/config", response_model=PracticeConfigResponse)
def practice_config() -> dict:
    return {
        "categories": [
            "adaptability",
            "career-goals",
            "conflict-resolution",
            "culture-fit",
            "leadership",
            "motivation",
            "team-collaboration",
            "work-style",
        ],
        "difficulties": ["easy", "medium", "hard"],
        "time_limits_sec": [30, 45, 60, 90, 120],
        "question_count_options": [5, 10, 15, 20],
    }

@router.post("/practice/sessions", response_model=SessionStateResponse)
def create_session(
    payload: CreateSessionRequest,
    user: dict = Depends(get_current_user),
) -> dict:
    try:
        session = store.create_session(
            user_id=user["id"],
            category=payload.category,
            difficulty=payload.difficulty,
            time_limit_sec=payload.time_limit_sec,
            question_count=payload.question_count,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _session_state(session)

@router.get("/practice/sessions/{session_id}", response_model=SessionStateResponse)
def get_session(session_id: str, user: dict = Depends(get_current_user)) -> dict:
    session = store.get_session(user_id=user["id"], session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return _session_state(session)

@router.post("/practice/sessions/{session_id}/start", response_model=SessionStateResponse)
def start_session(session_id: str, user: dict = Depends(get_current_user)) -> dict:
    session = store.get_session(user_id=user["id"], session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    started = store.start_session(session)
    return _session_state(started)

@router.post("/practice/sessions/{session_id}/finish", response_model=SessionStateResponse)
def finish_session(session_id: str, user: dict = Depends(get_current_user)) -> dict:
    session = store.get_session(user_id=user["id"], session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    finished = store.finish_session(session)
    return _session_state(finished)

@router.get("/practice/sessions/{session_id}/questions/current", response_model=SessionQuestionResponse)
def current_question(session_id: str, user: dict = Depends(get_current_user)) -> dict:
    session = store.get_session(user_id=user["id"], session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    question = store.get_current_question(session)
    return {
        "session_id": session_id,
        "current_question_index": session["current_question_index"],
        "total_questions": session["question_count"],
        "question": question,
    }

@router.post("/practice/sessions/{session_id}/questions/next", response_model=SessionQuestionResponse)
def next_question(session_id: str, user: dict = Depends(get_current_user)) -> dict:
    session = store.get_session(user_id=user["id"], session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    question = store.next_question(session)
    if question is None:
        raise HTTPException(status_code=409, detail="No next question. Session already at last question")

    return {
        "session_id": session_id,
        "current_question_index": session["current_question_index"],
        "total_questions": session["question_count"],
        "question": question,
    }

@router.post("/practice/sessions/{session_id}/answers", response_model=SubmitAnswerResponse)
def submit_answer(
    session_id: str,
    payload: SubmitAnswerRequest,
    user: dict = Depends(get_current_user),
) -> dict:
    session = store.get_session(user_id=user["id"], session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    answer, _analysis = store.submit_answer(
        session=session,
        question_id=payload.question_id,
        answer_text=payload.answer_text,
        audio_url=payload.audio_url,
        audio_id=payload.audio_id,
    )

    return {
        "answer_id": answer["id"],
        "session_id": session_id,
        "question_id": answer["question_id"],
        "status": answer["status"],
        "transcript": answer["transcript"],
    }


@router.post("/practice/sessions/{session_id}/audio", response_model=AudioUploadResponse)
def upload_answer_audio(
    session_id: str,
    payload: AudioUploadRequest,
    user: dict = Depends(get_current_user),
) -> dict:
    session = store.get_session(user_id=user["id"], session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if payload.question_id not in session["question_ids"]:
        raise HTTPException(status_code=409, detail="Question does not belong to this session")

    try:
        return audio_storage.upload_base64_audio(
            user_id=user["id"],
            session_id=session_id,
            question_id=payload.question_id,
            file_name=payload.file_name,
            content_type=payload.content_type,
            audio_base64=payload.audio_base64,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid audio payload") from exc
    except (BotoCoreError, ClientError, OSError) as exc:
        raise HTTPException(status_code=503, detail="Audio storage is unavailable") from exc

@router.get(
    "/practice/sessions/{session_id}/answers/{answer_id}/analysis",
    response_model=AnswerAnalysisResponse,
)
def get_analysis(session_id: str, answer_id: str, user: dict = Depends(get_current_user)) -> dict:
    session = store.get_session(user_id=user["id"], session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    analysis = store.get_analysis(session=session, answer_id=answer_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.get("/practice/sessions/{session_id}/results", response_model=SessionResultsResponse)
def session_results(session_id: str, user: dict = Depends(get_current_user)) -> dict:
    session = store.get_session(user_id=user["id"], session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return store.get_session_results(session)
