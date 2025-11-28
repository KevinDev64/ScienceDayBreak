import io
import math
from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Request
from fastapi import BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import async_get_db
from core.templates import default_template
from database import Event, Participant
from helpers import background_worker_async
from schemas import EventCreateForm, EventUpdateForm
from schemas.response import ParticipantResponse

router = APIRouter(prefix="/operator", tags=["Endpoints for operator"])


@router.post("/event")
async def create_event(
        background_tasks: BackgroundTasks,
        event_data: EventCreateForm = Depends(),
        db: AsyncSession = Depends(async_get_db),
):

    image_path = None
    if event_data.image:
        # Тут логика сохранения файла на диск
        # content = await event_data.image.read()
        # ... save to disk ...
        image_path = f"uploads/{event_data.image.filename}"
        print(f"📸 Получена картинка: {event_data.image.filename}")

    # 3. Сохранение в БД
    new_event = Event(
        name=event_data.name,
        date_str=event_data.date_str,
        template_html=default_template,
        description=event_data.description,
        image_path=image_path,
    )

    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)

    if event_data.csv_file:
        # Если нужно прочитать текст CSV
        content = await event_data.csv_file.read()
        decoded_content = content.decode('utf-8')
        print(f"📄 Получен CSV файл: {event_data.csv_file.filename}")
        # ... парсинг CSV ...

    return {
        "status": "success",
        "event_id": new_event.id,
        "message": "Событие создано",
        "files_received": {
            "image": event_data.image.filename if event_data.image else None,
            "csv": event_data.csv_file.filename if event_data.csv_file else None
        }
    }


@router.put("/event/{event_id}")
async def update_event(
        event_id: int,
        background_tasks: BackgroundTasks,
        event_data: EventUpdateForm = Depends(),
        db: AsyncSession = Depends(async_get_db)
):
    query = select(Event).where(Event.id == event_id)
    result = await db.execute(query)
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие не найдено"
        )

    # 2. Обновляем текстовые поля (только если они пришли)
    if event_data.name is not None:
        event.name = event_data.name

    if event_data.date_str is not None:
        event.date_str = event_data.date_str

    if event_data.description is not None:
        event.description = event_data.description

    # 3. Обработка файлов (если прислали новые)

    # Картинка
    if event_data.image:
        # Логика сохранения файла (как в create)
        # content = await event_data.image.read()
        # save_path = f"uploads/{event_data.image.filename}"
        # ... сохранить на диск ...

        print(f"📸 Обновлена картинка: {event_data.image.filename}")

        # Если в БД есть поле для пути к картинке, обновляем его
        # event.image_path = f"uploads/{event_data.image.filename}"

    # CSV файл
    if event_data.csv_file:

        content = await event_data.csv_file.read()
        decoded_content = content.decode('utf-8')
        print(f"📄 Обновлен CSV файл: {event_data.csv_file.filename}")


        # Тут можно запустить парсинг нового CSV и обновить участников
        # await parse_and_update_participants(decoded_content, event.id, db)

    # 4. Сохраняем изменения
    await db.commit()
    await db.refresh(event)

    return {
        "status": "success",
        "event_id": event.id,
        "message": "Событие обновлено",
    }


@router.get("/event/{event_id}/participants", response_model=List[ParticipantResponse])
async def get_event_participants(
        event_id: int,
        request: Request,
        db: AsyncSession = Depends(async_get_db)
):
    """
    Получить всех участников конкретного события.
    Если is_generated=True, добавляет ссылку на скачивание файла.
    """

    # 1. Делаем выборку по event_id
    query = select(Participant).where(Participant.event_id == event_id)
    result = await db.execute(query)
    participants = result.scalars().all()

    response_list = []

    for p in participants:
        download_link = None

        # 2. Логика формирования ссылки
        if p.is_generated and p.file_path:
            clean_path = p.file_path.lstrip("/")

            download_link = f"{request.base_url}static/{clean_path}"

        # 3. Собираем модель ответа вручную
        participant_resp = ParticipantResponse(
            id=p.id,
            event_id=p.event_id,
            name=p.name,
            email=p.email,
            role=p.role,
            place=p.place,
            is_generated=p.is_generated,
            is_sent=p.is_sent,
            download_url=download_link  # <-- Вставляем ссылку
        )
        response_list.append(participant_resp)

    return response_list


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


def safe_str(value):
    """Безопасное преобразование в строку"""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ''
    return str(value)


async def upload_file_to_db(event_id, file, background_tasks, db: AsyncSession):
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
    await start_background(event_id, background_tasks, db)


async def start_background(event_id, background_tasks, db: AsyncSession):
    result = await db.execute(
        select(Participant).filter(
            Participant.event_id == event_id,
            Participant.is_sent == False
        )
    )
    participants = result.scalars().all()

    if not participants:
        return {"message": "Нет участников для обработки"}

    background_tasks.add_task(background_worker_async, event_id)
