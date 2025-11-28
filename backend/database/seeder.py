# auth/seeder.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from database import User, Role
from helpers import hash_password

# Данные для сидинга
SEED_USERS = [
    {
        "email": "admin@example.com",
        "username": "admin",
        "password": "admin123",
        "role": Role.ADMIN,
    },
    {
        "email": "operator@example.com",
        "username": "operator",
        "password": "operator123",
        "role": Role.OPERATOR,
    },
    {
        "email": "user@example.com",
        "username": "user",
        "password": "user123",
        "role": Role.USER,
    },
]


async def seed_users(db: AsyncSession) -> dict:
    """Создаёт тестовых пользователей для каждой роли"""

    created = []
    skipped = []

    for user_data in SEED_USERS:
        # 1. Используем select() и or_() вместо db.query()
        query = select(User).where(
            or_(
                User.email == user_data["email"],
                User.username == user_data["username"]
            )
        )

        result = await db.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            skipped.append(user_data["email"])
            continue

        # Создаём пользователя (это остается без изменений)
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            hashed_password=hash_password(user_data["password"]),
            role=user_data["role"],
        )

        # db.add работает синхронно, так как просто добавляет объект в память сессии
        db.add(user)
        created.append(user_data["email"])

    # Сохраняем изменения в базу
    await db.commit()

    return {
        "created": created,
        "skipped": skipped,
    }


async def clear_users(db: Session) -> int:
    """Удаляет всех пользователей (осторожно!)"""
    count = db.query(User).delete()
    await db.commit()
    return count


async def run_seeder(db: AsyncSession):
    # Создаем новую сессию базы данных
    # Если у вас есть get_db() или async_session_maker, используйте их


    try:
        print("🌱 Запуск сидера...")
        print("-" * 40)

        # Выполняем асинхронную функцию сидинга
        result = await seed_users(db)

        if result.get("created"):
            print("✅ Созданы пользователи:")
            for email in result["created"]:
                print(f"   - {email}")

        if result.get("skipped"):
            print("⏭️  Пропущены (уже существуют):")
            for email in result["skipped"]:
                print(f"   - {email}")

        print("-" * 40)
        print("📋 Данные для входа:")
        print()

        for user_data in SEED_USERS:
            # Проверка на случай, если role это просто строка, а не Enum
            role_name = user_data['role']
            if hasattr(role_name, 'value'):
                role_name = role_name.value

            print(f"   {str(role_name).upper()}:")
            print(f"   Email: {user_data['email']}")
            print(f"   Password: {user_data['password']}")
            print()

        print("✨ Сидинг завершён!")

    except Exception as e:
        print(f"❌ Ошибка при сидинге: {e}")
        # Можно раскомментировать raise, чтобы видеть полный трейсбек ошибки
        # raise e
