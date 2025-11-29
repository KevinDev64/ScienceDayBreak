import datetime
from enum import Enum
from pydantic import ConfigDict
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import declarative_base, relationship

DeclBase = declarative_base()


class Event(DeclBase):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_str = Column(String)
    description = Column(String)
    image_path = Column(String, default=None, nullable=True)
    template_html = Column(String)


class Participant(DeclBase):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    name = Column(String)
    email = Column(String)
    role = Column(String)
    place = Column(String, nullable=True)
    is_generated = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    file_path = Column(String, nullable=True)

    event = relationship("Event")


class Role(str, Enum):
    model_config = ConfigDict(use_enum_values=True)
    USER = "user"
    ADMIN = "admin"
    OPERATOR = "operator"


class User(DeclBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(Role), default=Role.USER, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    is_active = Column(Integer, default=1)

    user_refresh_tokens = relationship("IssuedJWTToken", cascade="all,delete", back_populates="user")


class IssuedJWTToken(DeclBase):
    __tablename__ = "issued_jwt_token"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    jti = Column(String)
    revoked = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    modificated_date = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User", back_populates="user_refresh_tokens")


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(DeclBase.metadata.create_all)