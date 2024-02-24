"""..."""
import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from bgscoring.database import Base


class Game(Base):
    """..."""

    __tablename__ = "game"

    game_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    cells: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        """..."""
        return f"Game(game_id={self.game_id!r}, title={self.title!r})"
