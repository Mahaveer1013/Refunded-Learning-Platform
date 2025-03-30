from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.user import User, TokenBlacklist
from ..schemas.user import UserCreate
from ..utils.user import (
    get_password_hash,
    verify_password,
    create_token,
    decode_token
)
from ..core.config import settings

class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = AuthService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        
        # Update last login time
        user.last_login = datetime.now()
        db.commit()
        db.refresh(user)
        
        return user

    @staticmethod
    def create_tokens(user: User):
        token_expires = timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        
        token = create_token(
            data={"sub": user.email},
            expires_delta=token_expires
        )
        
        return {
            "token": token,
            "token_type": "bearer"
        }

    @staticmethod
    def logout(db: Session, token: str):
        payload = decode_token(token)
        if not payload:
            return
        
        expires_at = datetime.fromtimestamp(payload["exp"])
        db_token = TokenBlacklist(token=token, expires_at=expires_at)
        db.add(db_token)
        db.commit()

    @staticmethod
    def is_token_blacklisted(db: Session, token: str):
        return db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None