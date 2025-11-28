import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import async_get_db, ALGORITHM, SECRET_KEY
from database import User, Role, IssuedJWTToken
from helpers import hash_password, verify_password, create_access_token, create_refresh_token
from schemas import UserCreate, UserLogin, UserResponse, Token, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(async_get_db)):
    result = await db.execute(
        select(User).where(
            or_(
                User.email == user_data.email,
                User.username == user_data.username
            )
        )
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
        raise HTTPException(status_code=400, detail="Username уже занят")

    # Создание пользователя
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=Role.USER
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=Token)
async def login(
        user_data: UserLogin,
        db: AsyncSession = Depends(async_get_db)
):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = {"user_id": user.id, "role": user.role.value}

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)  # <-- вот он

    refresh_token_obj = IssuedJWTToken(
        user_id=user.id,
        jti=refresh_token
    )
    db.add(refresh_token_obj)
    await db.commit()

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/token/refresh", response_model=Token)
async def refresh_token(
        request: RefreshTokenRequest,
        db: AsyncSession = Depends(async_get_db)
):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Это не refresh token"
        )

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Некорректный токен")

    # Проверяем, что токен не отозван (если храним в БД)
    result = await db.execute(
        select(IssuedJWTToken).where(
            IssuedJWTToken.jti == request.refresh_token,
            IssuedJWTToken.user_id == user_id,
            IssuedJWTToken.revoked.is_(False),
            # RefreshToken.expires_at > datetime.utcnow()
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=401, detail="Refresh token отозван или истёк")

    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    new_payload = {"user_id": user.id, "role": user.role.value}

    return Token(
        access_token=create_access_token(new_payload),
        refresh_token=create_refresh_token(new_payload),
        user=UserResponse.model_validate(user)
    )