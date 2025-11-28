import io
import math

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi import BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.routes.user import EventCreate
from core.config import async_get_db
from database import Event, Participant
from helpers import background_worker_async

router = APIRouter(prefix="/operator", tags=["Endpoints for operator"])


@router.post("/event")
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


def safe_str(value):
    """Безопасное преобразование в строку"""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ''
    return str(value)


@router.post("/events/{event_id}/upload-csv")
async def upload_participants(event_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(async_get_db)):
    """
       Загрузка upload csv
    """
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    required_cols = ['name', 'email', 'role']
    if not all(col in df.columns for col in required_cols):
        raise HTTPException(status_code=400, detail="CSV должен содержать колонки name, email, role")

    count = 0
    for _, row in df.iterrows():
        participant = Participant(
            event_id=event_id,
            name=safe_str(row['name']),
            email=safe_str(row['email']),
            role=safe_str(row['role']),
            place=safe_str(row.get('place', ''))
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
    # Получаем данные внутри endpoint'а
    event = await db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    result = await db.execute(
        select(Participant).filter(
            Participant.event_id == event_id,
            Participant.is_sent == False
        )
    )
    participants = result.scalars().all()

    if not participants:
        return {"message": "Нет участников для обработки"}

    # Добавляем асинхронную задачу
    background_tasks.add_task(background_worker_async, event_id)

    return {"message": "Процесс генерации и рассылки запущен"}
