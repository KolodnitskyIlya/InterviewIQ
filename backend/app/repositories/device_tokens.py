from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device_token import DeviceToken


class DeviceTokenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert(
        self,
        user_id: str,
        token: str,
        platform: str,
        provider: str,
        app_version: str | None = None,
        device_id: str | None = None,
    ) -> DeviceToken:
        stmt = select(DeviceToken).where(DeviceToken.user_id == user_id, DeviceToken.token == token)
        existing = self.db.scalars(stmt).first()
        if existing:
            existing.platform = platform
            existing.provider = provider
            existing.app_version = app_version
            existing.device_id = device_id
            existing.updated_at = datetime.now(timezone.utc)
            self.db.flush()
            return existing

        device_token = DeviceToken(
            id=f"dt_{uuid4().hex[:12]}",
            user_id=user_id,
            token=token,
            platform=platform,
            provider=provider,
            app_version=app_version,
            device_id=device_id,
        )
        self.db.add(device_token)
        self.db.flush()
        return device_token

    def list_for_user(self, user_id: str) -> list[DeviceToken]:
        stmt = (
            select(DeviceToken)
            .where(DeviceToken.user_id == user_id)
            .order_by(DeviceToken.updated_at.desc())
        )
        return list(self.db.scalars(stmt).all())
