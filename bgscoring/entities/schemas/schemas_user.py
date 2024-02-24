import uuid

# from datetime import datetime, timezone
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field


class UserShow(BaseModel):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    hashed_password: bytes
    is_active: bool = True
    # is_verified: bool = False
    # date_joined: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # last_login: Optional[datetime] = None
    # avatar: Optional[HttpUrl] = None
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    # date_of_birth: Optional[datetime] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50, default=None)
    email: EmailStr
    password: str


class UserDelete(BaseModel):
    deleted_user_id: UUID4


class UserUpdate(BaseModel):
    username: Optional[str] = Field(min_length=1, max_length=50, default=None)
    email: Optional[EmailStr] = None


class UserForToken(BaseModel):
    """..."""

    email: EmailStr
    user_id: UUID4
