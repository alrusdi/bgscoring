from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Table,
    Column,
    JSON,
    Boolean,
)

from bgscoring.database import Base, metadata

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("perm", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("register_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=True, nullable=False),
    Column("is_verified", Boolean, default=True, nullable=False),
)


class User(SQLAlchemyBaseUserTable[Column[int]], Base):
    id = Column(Integer, primary_key=True)  # type: ignore
    email: Column[str] = Column(
        String(length=320), unique=True, index=True, nullable=False
    )  # type: ignore
    username = Column(String, nullable=False)  # type: ignore
    register_at = Column(TIMESTAMP, default=datetime.utcnow)  # type: ignore
    role_id = Column(Integer, ForeignKey(role.c.id))  # type: ignore
    hashed_password: str = Column(String(length=1024), nullable=False)  # type: ignore
    is_active: bool = Column(Boolean, default=True, nullable=False)  # type: ignore
    is_superuser: bool = Column(Boolean, default=True, nullable=False)  # type: ignore
    is_verified: bool = Column(Boolean, default=True, nullable=False)  # type: ignore
