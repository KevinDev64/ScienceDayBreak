from typing import Optional

from fastapi import Form, File, UploadFile
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


class EventResponse(BaseModel):
    id: int
    name: str
    date_str: str

    class Config:
        from_attributes = True


class EventDetailResponse(EventResponse):
    # Доп. инфо для детального просмотра, можно добавить статус участника
    user_role: str | None = None
    user_place: str | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class EventCreateForm:
    def __init__(
            self,
            name: str = Form(...),
            date_str: str = Form(...),
            description: str = Form(...),
            image: UploadFile = File(None),
            csv_file: UploadFile = File(None)
    ):
        self.name = name
        self.date_str = date_str
        self.description = description
        self.image = image
        self.csv_file = csv_file


class EventUpdateForm:
    def __init__(
            self,
            name: Optional[str] = Form(None),
            date_str: Optional[str] = Form(None),
            description: Optional[str] = Form(None),  # Если оно есть в модели
            image: Optional[UploadFile] = File(None),
            csv_file: Optional[UploadFile] = File(None)
    ):
        self.name = name
        self.date_str = date_str
        self.description = description
        self.image = image
        self.csv_file = csv_file
