# from datetime import datetime
#
# from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
# from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import Mapped
#
# from bgscoring.database import Base, str_256
# from bgscoring.games.models import uuidpk
#
#
# class Role(Base):
#     __tablename__ = "role"
#
#     id: Mapped[uuidpk]
#     name: Mapped[str_256]
#     permission: Mapped[str_256]
#
#
# class User(SQLAlchemyBaseUserTable[Column[int]], Base):
#     id = Column(Integer, primary_key=True)
#     email: Column[str] = Column(String(length=320), unique=True, index=True, nullable=False)
#     username = Column(String, nullable=False)
#     register_at = Column(TIMESTAMP, default=datetime.utcnow)
#     role_id = Column(Integer, ForeignKey(Role.id))
#     hashed_password: str = Column(String(length=1024), nullable=False)
#     is_active: bool = Column(Boolean, default=True, nullable=False)
#     is_superuser: bool = Column(Boolean, default=True, nullable=False)
#     is_verified: bool = Column(Boolean, default=True, nullable=False)
