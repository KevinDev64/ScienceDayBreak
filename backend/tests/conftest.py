from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import async_get_db
from database import DeclBase
from main import app

# Используем in-memory SQLite для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(DeclBase.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(DeclBase.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    # Переопределяем зависимость get_db
    async def override_get_db():
        yield db_session

    app.dependency_overrides[async_get_db] = override_get_db

    # 2. Создаем транспорт с вашим приложением
    transport = ASGITransport(app=app)

    # 3. Передаем transport вместо app
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session):
    """Создает тестового пользователя в БД"""
    # Предполагается, что вы импортировали модель User из database
    from database import User

    # 💥 ИСПРАВЛЕНО: Добавьте непустое значение для hashed_password
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="fake_hashed_password_for_tests",
        # ... другие обязательные поля, если они есть ...
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_headers(client, test_user):
    """
    Возвращает заголовки авторизации.
    Здесь нужно сымитировать токен или переопределить get_current_user.
    Для простоты теста часто переопределяют get_current_user.
    """
    from helpers import get_current_user
    app.dependency_overrides[get_current_user] = lambda: test_user
    return {}  # Заголовки пустые, т.к. мы подменили зависимость
