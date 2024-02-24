import uuid
from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field

from bgscoring.entities.enums import KeyAction


class KeyCreate(BaseModel):
    value: str
    display_value: Optional[str] = None
    data_type: Decimal
    action: KeyAction


class KeyShow(BaseModel):
    key_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    value: str
    display_value: Optional[str] = None
    data_type: Decimal
    action: KeyAction


class KeyUpdate(BaseModel):
    value: Optional[str] = None
    display_value: Optional[str] = None
    data_type: Decimal
    action: KeyAction


class KeyDelete(BaseModel):
    deleted_key_id: UUID4
