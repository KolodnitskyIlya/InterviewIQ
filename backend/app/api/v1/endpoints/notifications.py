from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.db.session import SessionLocal
from app.repositories.device_tokens import DeviceTokenRepository
from app.schemas.notification import ReminderTestRequest, ReminderTestResponse
from app.services.notifications import notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/test-reminder", response_model=ReminderTestResponse)
def send_test_reminder(
    payload: ReminderTestRequest,
    user: dict = Depends(get_current_user),
) -> dict:
    db = SessionLocal()
    try:
        tokens = DeviceTokenRepository(db).list_for_user(user["id"])
        results = []
        for token in tokens:
            result = notification_service.send_reminder(token, title=payload.title, body=payload.body)
            results.append(
                {
                    "token_id": token.id,
                    "provider": result.provider,
                    "success": result.success,
                    "message_id": result.message_id,
                    "error": result.error,
                }
            )

        return {
            "sent": len([item for item in results if item["success"]]),
            "failed": len([item for item in results if not item["success"]]),
            "results": results,
        }
    finally:
        db.close()
