from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class UserPublic(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    created_at: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AuthResponse(BaseModel):
    user: UserPublic
    tokens: TokenPair
