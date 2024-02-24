import datetime
import uuid
from enum import Enum
from typing import Annotated

from sqlalchemy import DECIMAL, UUID, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bgscoring.database import Base, str_256

uuidpk = Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class KeyAction(Enum):
    VALUE = 'value'
    MATH_OP = 'math_op'


class Key(Base):
    __tablename__ = "key"

    id: Mapped[uuidpk]
    value: Mapped[str_256]
    display_value: Mapped[str_256]
    data_type: Mapped[DECIMAL]
    action: Mapped[KeyAction]


class Keyboard(Base):
    __tablename__ = "keyboard"

    id: Mapped[uuidpk]
    title: Mapped[str_256]
    keys: relationship("Key")


class MathOp(Enum):
    MINUS = 'minus'
    PLUS = 'plus'


class Cell(Base):
    __tablename__ = "cell"

    id: Mapped[uuidpk]
    keyboard: relationship("Keyboard")
    math_op: Mapped[MathOp]


class Game(Base):
    __tablename__ = "game"

    id: Mapped[uuidpk]
    title: Mapped[str_256]
    cells: relationship("Cell")


class GameResult(Base):
    __tablename__ = "game_result"

    id: Mapped[uuidpk]
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id", nullable=False))
    created_at: Mapped[created_at]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', nullable=True))
    session_id: Mapped[str_256] = mapped_column(nullable=True)
    players: relationship("GamePlayer")


class PlayerColor(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    YELLOW = 'yellow'
    BLACK = 'black'


class GamePlayer(Base):
    __tablename__ = "game_player"

    id: Mapped[uuidpk]
    color: Mapped[PlayerColor]
    name: Mapped[str_256]
    values: Mapped[DECIMAL]
