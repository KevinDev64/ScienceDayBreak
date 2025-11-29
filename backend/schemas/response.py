from typing import Optional

from pydantic import BaseModel

from database import Role


class ParticipantResponse(BaseModel):
    id: int
    event_id: int
    name: str
    email: str
    role: str
    place: Optional[str] = None
    is_generated: bool
    is_sent: bool
    download_url: Optional[str] = None

    class Config:
        from_attributes = True


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
