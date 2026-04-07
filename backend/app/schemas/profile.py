from pydantic import BaseModel, EmailStr, Field


class UserProfileResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    target_role: str | None
    experience_level: str | None
    created_at: str
    updated_at: str


class UpdateProfileRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    target_role: str | None = None
    experience_level: str | None = None
