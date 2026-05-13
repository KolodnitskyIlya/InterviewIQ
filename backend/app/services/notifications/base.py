from dataclasses import dataclass

@dataclass(frozen=True)
class NotificationMessage:
    title: str
    body: str
    data: dict[str, str] | None = None

@dataclass(frozen=True)
class NotificationResult:
    success: bool
    provider: str
    message_id: str | None = None
    error: str | None = None

class NotificationProvider:
    provider_name = "base"

    def send(self, token: str, message: NotificationMessage) -> NotificationResult:
        raise NotImplementedError
