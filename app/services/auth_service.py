from app.models.user import User
from app.core.hashing import Hasher
from app.core.security import  create_access_token
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from datetime import timedelta
from typing import Optional


class AuthService:

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.username == username, User.is_deleted == False).first()
        if not user:
            return None
        if not Hasher.verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def login(db: Session, username: str, password: str) -> Optional[str]:
        user = AuthService.authenticate_user(db, username, password)
        if not user:
            return None

        access_token_expires = timedelta(minutes=settings.JWT_EXPIRES_MINUTES)

        token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )

        return token
