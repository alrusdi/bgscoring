from datetime import datetime, timezone
import uuid
from typing import Optional

from pydantic import ConfigDict, EmailStr, Field, HttpUrl, BaseModel


class User(BaseModel):
    id: uuid
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False
    date_joined: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None
    avatar: Optional[HttpUrl] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)
