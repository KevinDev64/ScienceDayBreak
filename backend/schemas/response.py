from pydantic import BaseModel
from typing import Optional


class ParticipantResponse(BaseModel):
    id: int
    event_id: int
    name: str
    email: str
    role: str
    place: Optional[str] = None
    is_generated: bool
    is_sent: bool

    # Поле для ссылки
    download_url: Optional[str] = None

    class Config:
        from_attributes = True