import logging
import os
from logging.config import dictConfig
from typing import AsyncGenerator

from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from starlette.config import Config
from starlette.datastructures import Secret

from database.db_session import get_db_path
from .logging import logging_config

config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=str, default="your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

MEMOIZATION_FLAG: bool = config("MEMOIZATION_FLAG", cast=bool, default=True)

HOST: str = config("HOST", cast=str, default="localhost")
PORT: int = config("PORT", cast=int, default=8000)
PROJECT_NAME: str = config("PROJECT_NAME", default="ScienceDayBreak")

POSTGRES_HOST: str = config("POSTGRES_HOST", cast=str, default="localhost")
POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int, default=5432)
POSTGRES_USER: str = config("POSTGRES_USER", cast=str, default="postgres")
POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str, default="<PASSWORD>")
POSTGRES_DB: str = config("POSTGRES_DATABASE", cast=str, default="postgres")

SMTP_HOST = config("SMTP_HOST", default="smtp.gmail.com")
SMTP_PORT = config("SMTP_PORT", default=587, cast=int)
SMTP_USER = config("SMTP_USER", cast=str, default="<EMAIL>")
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=str, default="<PASSWORD>")
SMTP_FROM_NAME = config("SMTP_FROM_NAME", default="Event Service")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
PATH_DB = get_db_path(POSTGRES_USER, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB,
                      POSTGRES_PASSWORD)
engine = create_async_engine(PATH_DB)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

security = HTTPBearer()


async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as db:
        yield db




# logging configuration
# LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
# logging.basicConfig(
#     handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
# )
# logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

dictConfig(logging_config)

# Создаем экземпляр логгера для нашего модуля
logger = logging.getLogger(__name__)
