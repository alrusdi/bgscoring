from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData

from src.database import metadata

games = Table(
    "games",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("figi", String),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP),
    Column("type", String),
)