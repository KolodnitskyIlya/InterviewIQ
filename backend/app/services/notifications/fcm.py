import json
import urllib.error
import urllib.request
from app.services.notifications.base import NotificationMessage, NotificationProvider, NotificationResult

class FcmNotificationProvider(NotificationProvider):
    provider_name = "fcm"

    def __init__(self, server_key: str = "") -> None:
        self.server_key = server_key

    def send(self, token: str, message: NotificationMessage) -> NotificationResult:
        if not self.server_key:
            return NotificationResult(success=False, provider=self.provider_name, error="FCM_SERVER_KEY is missing")

        payload = {
            "to": token,
            "notification": {
                "title": message.title,
                "body": message.body,
            },
            "data": message.data or {},
        }
        request = urllib.request.Request(
            "https://fcm.googleapis.com/fcm/send",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"key={self.server_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
                return NotificationResult(
                    success=True,
                    provider=self.provider_name,
                    message_id=str(data.get("message_id") or data.get("multicast_id")),
                )
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            return NotificationResult(success=False, provider=self.provider_name, error=f"{exc.code}: {detail}")
        except Exception as exc:
            return NotificationResult(success=False, provider=self.provider_name, error=str(exc))
