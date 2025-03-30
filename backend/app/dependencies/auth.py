from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from ..core.database import get_db
from ..schemas.user import TokenData
from ..core.config import settings
from ..services.auth import AuthService
from ..models.user import User

security = HTTPBearer()


async def get_token(request: Request) -> str:
    credentials: HTTPAuthorizationCredentials = await security(request)
    print(credentials)
    return credentials.credentials


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(get_token)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    blacklisted = AuthService.is_token_blacklisted(db, token)
    if blacklisted:
        print(f"Is token blacklisted? {blacklisted}")
        raise credentials_exception

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = AuthService.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_superuser(current_user: User = Depends(get_current_active_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
