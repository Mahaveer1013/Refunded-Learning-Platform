from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..core.database import get_db
from ..schemas.user import (
    UserCreate,
    UserInDB,
    Token,
    PasswordResetRequest,
    PasswordReset,
)
from ..services.auth import AuthService
from ..dependencies.auth import get_current_active_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = AuthService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return AuthService.create_user(db=db, user=user)


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest, db: Session = Depends(get_db)
):
    user = AuthService.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthService.create_tokens(user)


@router.post("/logout")
async def logout(
    request: Request,
    db: Session = Depends(get_db),
):
    # Get token from Authorization header
    credentials: HTTPAuthorizationCredentials = await security(request)
    token = credentials.credentials

    AuthService.logout(db, token)
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/request-password-reset")
async def request_password_reset(
    request: PasswordResetRequest, db: Session = Depends(get_db)
):
    # Implement password reset logic (send email with reset link)
    return {
        "message": "If your email exists in our system, you'll receive a reset link"
    }


@router.post("/reset-password")
async def reset_password(reset_data: PasswordReset, db: Session = Depends(get_db)):
    # Implement password reset verification and update
    return {"message": "Password has been reset successfully"}
