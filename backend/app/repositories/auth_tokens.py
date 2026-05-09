from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.auth_token import AuthToken
from app.models.user import User

class AuthTokenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user_id: str, token: str, token_type: str) -> AuthToken:
        auth_token = AuthToken(user_id=user_id, token=token, token_type=token_type)
        self.db.add(auth_token)
        self.db.flush()
        return auth_token

    def get_user_by_token(self, token: str, token_type: str = "access") -> User | None:
        stmt = (
            select(User)
            .join(AuthToken, AuthToken.user_id == User.id)
            .where(AuthToken.token == token, AuthToken.token_type == token_type)
        )
        return self.db.scalars(stmt).first()
