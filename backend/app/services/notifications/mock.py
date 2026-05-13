import logging
from uuid import uuid4
from app.services.notifications.base import NotificationMessage, NotificationProvider, NotificationResult

logger = logging.getLogger("interviewiq.notifications")

class MockNotificationProvider(NotificationProvider):
    provider_name = "mock"

    def send(self, token: str, message: NotificationMessage) -> NotificationResult:
        message_id = f"mock_{uuid4().hex[:12]}"
        logger.info(
            "Mock notification sent",
            extra={
                "token": token[-8:],
                "title": message.title,
                "message_id": message_id,
            },
        )
        return NotificationResult(success=True, provider=self.provider_name, message_id=message_id)
