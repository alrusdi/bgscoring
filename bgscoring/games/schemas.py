from datetime import datetime

from pydantic import BaseModel


class GamesCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str
