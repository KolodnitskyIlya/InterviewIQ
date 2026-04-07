from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import AuthResponse, SignInRequest, SignUpRequest
from app.services.store import store

router = APIRouter(prefix="/auth", tags=["auth"])

def _public_user(user: dict) -> dict:
    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "created_at": user["created_at"],
    }

@router.post("/sign-up", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def sign_up(payload: SignUpRequest) -> dict:
    try:
        user = store.create_user(
            full_name=payload.full_name,
            email=payload.email,
            password=payload.password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    tokens = store.issue_tokens(user["id"])
    return {
        "user": _public_user(user),
        "tokens": tokens,
    }

@router.post("/sign-in", response_model=AuthResponse)
def sign_in(payload: SignInRequest) -> dict:
    user = store.authenticate(email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    tokens = store.issue_tokens(user["id"])
    return {
        "user": _public_user(user),
        "tokens": tokens,
    }
