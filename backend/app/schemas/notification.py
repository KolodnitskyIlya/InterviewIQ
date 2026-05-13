from pydantic import BaseModel

class ReminderTestRequest(BaseModel):
    title: str = "InterviewIQ"
    body: str = "Time to practice your interview answers."

class NotificationSendResult(BaseModel):
    token_id: str
    provider: str
    success: bool
    message_id: str | None = None
    error: str | None = None

class ReminderTestResponse(BaseModel):
    sent: int
    failed: int
    results: list[NotificationSendResult]
