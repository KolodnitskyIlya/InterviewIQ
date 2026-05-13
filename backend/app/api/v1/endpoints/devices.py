from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.db.session import SessionLocal
from app.repositories.device_tokens import DeviceTokenRepository
from app.schemas.device import DeviceTokenListResponse, DeviceTokenRegisterRequest, DeviceTokenResponse

router = APIRouter(prefix="/users/me/device-tokens", tags=["devices"])

def _device_token_response(token) -> dict:
    return {
        "id": token.id,
        "token": token.token,
        "platform": token.platform,
        "provider": token.provider,
        "app_version": token.app_version,
        "device_id": token.device_id,
        "created_at": token.created_at.isoformat(),
        "updated_at": token.updated_at.isoformat(),
    }

@router.post("", response_model=DeviceTokenResponse)
def register_device_token(
    payload: DeviceTokenRegisterRequest,
    user: dict = Depends(get_current_user),
) -> dict:
    db = SessionLocal()
    try:
        token = DeviceTokenRepository(db).upsert(
            user_id=user["id"],
            token=payload.token,
            platform=payload.platform,
            provider=payload.provider,
            app_version=payload.app_version,
            device_id=payload.device_id,
        )
        db.commit()
        return _device_token_response(token)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@router.get("", response_model=DeviceTokenListResponse)
def list_device_tokens(user: dict = Depends(get_current_user)) -> dict:
    db = SessionLocal()
    try:
        tokens = DeviceTokenRepository(db).list_for_user(user["id"])
        return {"items": [_device_token_response(token) for token in tokens]}
    finally:
        db.close()
