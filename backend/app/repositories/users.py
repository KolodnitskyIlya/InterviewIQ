from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, full_name: str, email: str, password: str) -> User:
        user = User(
            id=f"u_{uuid4().hex[:12]}",
            full_name=full_name.strip(),
            email=email.strip().lower(),
            password=password,
            onboarding_updated_at=datetime.now(timezone.utc),
        )
        self.db.add(user)
        self.db.flush()
        return user

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email.strip().lower())
        return self.db.scalars(stmt).first()

    def update_onboarding(self, user_id: str, role: str, experience_level: str) -> User:
        user = self.db.get(User, user_id)
        if user is None:
            raise ValueError("User not found")

        now = datetime.now(timezone.utc)
        user.target_role = role
        user.experience_level = experience_level
        user.onboarding_updated_at = now
        user.updated_at = now
        self.db.flush()
        return user

    def update_profile(
        self,
        user_id: str,
        full_name: str | None,
        target_role: str | None,
        experience_level: str | None,
    ) -> User:
        user = self.db.get(User, user_id)
        if user is None:
            raise ValueError("User not found")

        if full_name is not None:
            user.full_name = full_name.strip()
        if target_role is not None:
            user.target_role = target_role
        if experience_level is not None:
            user.experience_level = experience_level
        user.updated_at = datetime.now(timezone.utc)
        self.db.flush()
        return user
