"""..."""
import uuid
from decimal import Decimal

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from bgscoring.database import Base
from bgscoring.entities.enums import KeyAction


class Key(Base):
    """..."""

    __tablename__ = "key"

    key_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    value: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    display_value: Mapped[str]
    data_type: Mapped[Decimal]
    action: Mapped[KeyAction]

    def __repr__(self) -> str:
        """..."""
        return f"Key(key_id={self.key_id!r}, title={self.value!r})"
