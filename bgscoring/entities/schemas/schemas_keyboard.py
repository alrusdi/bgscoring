from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from bgscoring.entities.schemas.schemas_key import KeyShow


class KeyboardCreate(BaseModel):
    title: str
    keys: List[KeyShow]


class KeyboardShow(BaseModel):
    title: str
    keys: List[KeyShow]


class KeyboardUpdate(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=255, default=None)
    keys: List[KeyShow]


class KeyboardDelete(BaseModel):
    deleted_keyboard_id: UUID4
