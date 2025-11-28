import io

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

import worker
from core.config import async_get_db
from core.constants import require_user
from database import Event, Participant, User
from helpers import get_current_user
from schemas import UserResponse

router = APIRouter(tags=["user"], prefix="/user")


class EventCreate(BaseModel):
    name: str
    date_str: str


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/my-orders")
def get_my_orders(user: User = Depends(require_user)):
    """Доступно: user, operator, admin"""
    return {
        "user_id": user.id,
        "orders": [
            {"id": 1, "status": "pending"},
            {"id": 2, "status": "completed"}
        ]
    }


# --- Routes ---

@router.post("/events/")
async def create_event(event: EventCreate, db: AsyncSession = Depends(async_get_db)):
    # Для MVP загружаем дефолтный шаблон сразу
    default_template = """
    <html>
    <body style="border: 10px solid #333; padding: 20px; text-align: center;">
        <h1>СЕРТИФИКАТ</h1>
        <h3>Вручается</h3>
        <h2>{{ name }}</h2>
        <p>За участие в мероприятии: <b>{{ event_name }}</b></p>
        <p>Роль: {{ role }}</p>
        <p>Дата: {{ date }}</p>
    </body>
    </html>
    """
    db_event = Event(name=event.name, date_str=event.date_str, template_html=default_template)
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


@router.post("/events/{event_id}/upload-csv")
async def upload_participants(event_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(async_get_db)):
    # Читаем CSV
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    # Валидация колонок (упрощено)
    required_cols = ['name', 'email', 'role']
    if not all(col in df.columns for col in required_cols):
        raise HTTPException(status_code=400, detail="CSV должен содержать колонки name, email, role")

    # Сохранение в БД
    count = 0
    for _, row in df.iterrows():
        participant = Participant(
            event_id=event_id,
            name=row['name'],
            email=row['email'],
            role=row['role'],
            place=row.get('place', '')
        )
        db.add(participant)
        count += 1

    await db.commit()
    return {"message": f"Загружено {count} участников"}


@router.post("/events/{event_id}/process")
async def process_certificates(event_id: int, background_tasks: BackgroundTasks,
                               db: AsyncSession = Depends(async_get_db)):
    """
    Запускает фоновую задачу: генерация PDF + "отправка" почты
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    participants = db.query(Participant).filter(
        Participant.event_id == event_id,
        Participant.is_sent == False
    ).all()

    if not participants:
        return {"message": "Нет участников для обработки"}

    # Добавляем задачу в фон, чтобы не блокировать интерфейс
    background_tasks.add_task(background_worker, db, event, participants)

    return {"message": "Процесс генерации и рассылки запущен"}


def background_worker(db, event, participants):
    for p in participants:
        # 1. Генерация
        path = worker.generate_certificate_pdf(p, event)
        if path:
            p.file_path = path
            p.is_generated = True

            # 2. Отправка
            sent = worker.send_email_mock(p.email, path)
            if sent:
                p.is_sent = True

            db.commit()
