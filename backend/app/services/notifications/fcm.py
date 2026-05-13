import json
import urllib.error
import urllib.request
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from app.core.config import BASE_DIR
from app.services.notifications.base import NotificationMessage, NotificationProvider, NotificationResult

FCM_SCOPE = "https://www.googleapis.com/auth/firebase.messaging"

class FcmNotificationProvider(NotificationProvider):
    provider_name = "fcm"

    def __init__(self, project_id: str = "", service_account_path: str = "") -> None:
        self.project_id = project_id
        self.service_account_path = service_account_path
        self._credentials = None

    def _service_account_file(self) -> Path:
        path = Path(self.service_account_path)
        if path.is_absolute():
            return path
        return BASE_DIR / path

    def _load_credentials(self):
        if self._credentials is None:
            service_account_file = self._service_account_file()
            self._credentials = service_account.Credentials.from_service_account_file(
                service_account_file,
                scopes=[FCM_SCOPE],
            )

            if not self.project_id:
                with service_account_file.open("r", encoding="utf-8") as file:
                    self.project_id = json.load(file).get("project_id", "")

        return self._credentials

    def _access_token(self) -> str:
        credentials = self._load_credentials()
        if not credentials.valid:
            credentials.refresh(Request())
        return credentials.token

    def send(self, token: str, message: NotificationMessage) -> NotificationResult:
        if not self.service_account_path:
            return NotificationResult(
                success=False,
                provider=self.provider_name,
                error="FCM_SERVICE_ACCOUNT_PATH is missing",
            )
        if not self.project_id:
            return NotificationResult(success=False, provider=self.provider_name, error="FCM_PROJECT_ID is missing")

        payload = {
            "message": {
                "token": token,
                "notification": {
                    "title": message.title,
                    "body": message.body,
                },
                "data": message.data or {},
                "android": {
                    "priority": "HIGH",
                    "notification": {
                        "channel_id": "practice_reminders",
                    },
                },
            }
        }
        request = urllib.request.Request(
            f"https://fcm.googleapis.com/v1/projects/{self.project_id}/messages:send",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._access_token()}",
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
                    message_id=str(data.get("name")),
                )
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            return NotificationResult(success=False, provider=self.provider_name, error=f"{exc.code}: {detail}")
        except Exception as exc:
            return NotificationResult(success=False, provider=self.provider_name, error=str(exc))
