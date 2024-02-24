"""..."""
import uuid
from decimal import Decimal

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from bgscoring.database import Base
from bgscoring.entities.enums import PlayerColor


class GamePlayer(Base):
    """..."""

    __tablename__ = "game_player"

    game_player_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    color: Mapped[PlayerColor]
    name: Mapped[str]
    values: Mapped[Decimal]

    def __repr__(self) -> str:
        """..."""
        return f"GamePlayer(game_player_id={self.game_player_id!r}, color={self.color!r}, name={self.name!r}, \
        values={self.values!r})"
