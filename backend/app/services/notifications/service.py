from app.core.config import settings
from app.models.device_token import DeviceToken
from app.services.notifications.base import NotificationMessage, NotificationResult
from app.services.notifications.fcm import FcmNotificationProvider
from app.services.notifications.mock import MockNotificationProvider

class NotificationService:
    def __init__(self) -> None:
        self.mock = MockNotificationProvider()
        self.fcm = FcmNotificationProvider(
            project_id=settings.fcm_project_id,
            service_account_path=settings.fcm_service_account_path,
        )

    def send_reminder(self, device_token: DeviceToken, title: str, body: str) -> NotificationResult:
        message = NotificationMessage(
            title=title,
            body=body,
            data={"type": "practice_reminder"},
        )

        if device_token.provider == "fcm":
            return self.fcm.send(device_token.token, message)

        return self.mock.send(device_token.token, message)

notification_service = NotificationService()
