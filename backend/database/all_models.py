import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import declarative_base, relationship

DeclBase = declarative_base()


class Event(DeclBase):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_str = Column(String)  # Дата выдачи текстом
    template_html = Column(String)  # Храним HTML код шаблона прямо в БД для простоты


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


async def create_tables(engine: AsyncEngine):
    # DeclBase.metadata.create_all()
    async with engine.begin() as conn:
        await conn.run_sync(DeclBase.metadata.create_all)
