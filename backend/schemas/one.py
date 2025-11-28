# auth/schemas.py
from pydantic import BaseModel, EmailStr

from database import Role


# Запросы
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: Role

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse  # Добавляем пользователя


class TokenData(BaseModel):
    user_id: int | None = None
    role: Role | None = None
