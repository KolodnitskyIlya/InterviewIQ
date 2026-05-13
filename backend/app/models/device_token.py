from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class DeviceToken(Base):
    __tablename__ = "device_tokens"
    __table_args__ = (
        UniqueConstraint("user_id", "token", name="uq_device_tokens_user_token"),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    token: Mapped[str] = mapped_column(String(512), nullable=False)
    platform: Mapped[str] = mapped_column(String(20), nullable=False)
    provider: Mapped[str] = mapped_column(String(40), nullable=False, default="mock")
    app_version: Mapped[str | None] = mapped_column(String(40), nullable=True)
    device_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User")
