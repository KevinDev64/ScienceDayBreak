import io
import os
import zipfile

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.responses import FileResponse, StreamingResponse

from core.config import async_get_db
from database import Event, Participant, User
from helpers import get_current_user
from schemas import EventResponse, EventDetailResponse

router = APIRouter(tags=["user"], prefix="/user")


# 1) Получить все ивенты, где пользователь участвовал
@router.get("/events", response_model=list[EventResponse])
async def get_my_events(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(async_get_db)
):
    """
    Возвращает список мероприятий, в которых участвовал текущий пользователь.
    Связь ищется по email.
    """
    # Делаем JOIN: Event -> Participant, фильтруем по email пользователя
    stmt = (
        select(Event)
        .join(Participant, Participant.event_id == Event.id)
        .where(Participant.email == current_user.email)
    )
    result = await db.execute(stmt)
    events = result.scalars().all()
    return events


# 2) Получить инфу по конкретному хакатону (ивенту)
@router.get("/events/{event_id}/info", response_model=EventDetailResponse)
async def get_event_info(
        event_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(async_get_db)
):
    """
    Возвращает информацию о хакатоне и роль/статус текущего пользователя в нем.
    """
    # Получаем ивент
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")

    # Получаем данные об участии пользователя в этом ивенте
    p_stmt = select(Participant).where(
        Participant.event_id == event_id,
        Participant.email == current_user.email
    )
    p_result = await db.execute(p_stmt)
    participant = p_result.scalar_one_or_none()

    # Формируем ответ
    response = EventDetailResponse.from_orm(event)
    if participant:
        response.user_role = participant.role
        response.user_place = participant.place

    return response


# 3) Получить сертификат по конкретному эвенту
@router.get("/events/{event_id}/certificate")
async def download_event_certificate(
        event_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(async_get_db)
):
    """
    Скачивает PDF сертификат для конкретного события.
    """
    # Ищем участника
    stmt = select(Participant).where(
        Participant.event_id == event_id,
        Participant.email == current_user.email
    )
    result = await db.execute(stmt)
    participant = result.scalar_one_or_none()

    if not participant:
        raise HTTPException(status_code=404, detail="Вы не являетесь участником этого события")

    if not participant.is_generated or not participant.file_path:
        raise HTTPException(status_code=400, detail="Сертификат еще не готов")

    if not os.path.exists(participant.file_path):
        raise HTTPException(status_code=500, detail="Файл сертификата не найден на сервере")

    filename = os.path.basename(participant.file_path)
    return FileResponse(
        path=participant.file_path,
        filename=filename,
        media_type='application/pdf'
    )


@router.get("/my-certificates/download-all")
async def download_all_certificates_zip(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(async_get_db)
):
    """
    Собирает все готовые сертификаты пользователя в один ZIP архив.
    """
    # Находим всех участников с этим email, у которых есть готовые файлы
    stmt = (
        select(Participant)
        .join(Event, Participant.event_id == Event.id)  # Джойн нужен, чтобы получить имя ивента для названия файла
        .where(
            Participant.email == current_user.email,
            Participant.is_generated == True,
            Participant.file_path.isnot(None)
        )
    )
    # Чтобы получить доступ к полям Event внутри цикла, лучше сразу подгрузить
    stmt = stmt.options(selectinload(Participant.event))

    result = await db.execute(stmt)
    participants = result.scalars().all()

    if not participants:
        raise HTTPException(status_code=404, detail="Нет готовых сертификатов для скачивания")

    # Создаем ZIP в памяти
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        files_added = 0
        for p in participants:
            if p.file_path and os.path.exists(p.file_path):
                # Формируем красивое имя файла внутри архива: EventName_Role.pdf
                # Очистка имени от недопустимых символов для файловой системы
                safe_event_name = "".join([c for c in p.event.name if c.isalnum() or c in (' ', '-', '_')]).strip()
                archive_filename = f"{safe_event_name}_{p.role}.pdf"

                zip_file.write(p.file_path, arcname=archive_filename)
                files_added += 1

    if files_added == 0:
        raise HTTPException(status_code=500, detail="Файлы сертификатов отсутствуют на диске")

    # Возвращаем указатель в начало потока
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=my_certificates.zip"}
    )
