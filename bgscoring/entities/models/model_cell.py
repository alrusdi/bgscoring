"""..."""
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from bgscoring.database import Base
from bgscoring.entities.enums import MathOp


class Cell(Base):
    """..."""

    __tablename__ = "cell"

    cell_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    keyboard: Mapped[str]
    math_op: Mapped[MathOp]

    def __repr__(self) -> str:
        """..."""
        return f"Cell(cell_id={self.cell_id!r})"
