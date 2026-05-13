from pydantic import BaseModel, Field

class DeviceTokenRegisterRequest(BaseModel):
    token: str = Field(min_length=8, max_length=512)
    platform: str
    provider: str = "mock"
    app_version: str | None = None
    device_id: str | None = None

class DeviceTokenResponse(BaseModel):
    id: str
    token: str
    platform: str
    provider: str
    app_version: str | None
    device_id: str | None
    created_at: str
    updated_at: str

class DeviceTokenListResponse(BaseModel):
    items: list[DeviceTokenResponse]
