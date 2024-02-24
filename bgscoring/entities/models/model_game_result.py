"""..."""
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from bgscoring.database import Base


class GameResult(Base):
    """..."""

    __tablename__ = "game_result"

    game_result_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    game: Mapped[str]
    created_at: Mapped[str]
    author: Mapped[str]
    session_id: Mapped[str]
    players: Mapped[str]

    def __repr__(self) -> str:
        """..."""
        return f"GameResult(game_result_id={self.game_result_id!r}, game={self.game!r}, players={self.players!r})"
