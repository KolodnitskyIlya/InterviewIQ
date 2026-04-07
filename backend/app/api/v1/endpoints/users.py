from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.schemas.onboarding import (
    OnboardingOptionsResponse,
    OnboardingStateResponse,
    OnboardingUpdateRequest,
)
from app.schemas.profile import UpdateProfileRequest, UserProfileResponse
from app.services.store import store

router = APIRouter(tags=["users"])

@router.get("/onboarding/options", response_model=OnboardingOptionsResponse)
def onboarding_options() -> dict:
    return {
        "roles": ["ML Engineer", "Backend Engineer", "Data Scientist", "Product Analyst"],
        "experience_levels": ["junior", "middle", "senior"],
        "categories": ["technical", "behavioral", "system-design", "hr"],
    }

@router.put("/users/me/onboarding", response_model=OnboardingStateResponse)
def set_onboarding(
    payload: OnboardingUpdateRequest,
    user: dict = Depends(get_current_user),
) -> dict:
    return store.update_onboarding(
        user_id=user["id"],
        role=payload.role,
        experience_level=payload.experience_level,
    )

@router.get("/users/me/profile", response_model=UserProfileResponse)
def get_profile(user: dict = Depends(get_current_user)) -> dict:
    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "target_role": user["target_role"],
        "experience_level": user["experience_level"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }

@router.put("/users/me/profile", response_model=UserProfileResponse)
def update_profile(
    payload: UpdateProfileRequest,
    user: dict = Depends(get_current_user),
) -> dict:
    updated = store.update_profile(
        user_id=user["id"],
        full_name=payload.full_name,
        target_role=payload.target_role,
        experience_level=payload.experience_level,
    )
    return {
        "id": updated["id"],
        "full_name": updated["full_name"],
        "email": updated["email"],
        "target_role": updated["target_role"],
        "experience_level": updated["experience_level"],
        "created_at": updated["created_at"],
        "updated_at": updated["updated_at"],
    }

@router.get("/auth/me")
def auth_me(user: dict = Depends(get_current_user)) -> dict:
    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "target_role": user["target_role"],
        "experience_level": user["experience_level"],
        "created_at": user["created_at"],
    }
