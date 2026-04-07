from pydantic import BaseModel

class OnboardingOptionsResponse(BaseModel):
    roles: list[str]
    experience_levels: list[str]
    categories: list[str]

class OnboardingUpdateRequest(BaseModel):
    role: str
    experience_level: str

class OnboardingStateResponse(BaseModel):
    role: str | None
    experience_level: str | None
    updated_at: str
