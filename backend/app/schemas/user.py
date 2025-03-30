from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone: str = Field(..., min_length=10, max_length=15)

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Phone must contain only digits")
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)

    @field_validator("confirm_password", mode="before")
    @classmethod
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v

class UserInDB(UserBase):
    id: int
    is_active: bool = False
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True  # Updated for Pydantic v2

class Token(BaseModel):
    token:str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)
