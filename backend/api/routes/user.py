import os
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse, StreamingResponse

from core.config import async_get_db, logger
from database import Event, Participant, User
from helpers import get_current_user, CreateZipService
from schemas import EventResponse, EventDetailResponse

router = APIRouter(tags=["user"], prefix="/user")


@router.get("/events", response_model=list[EventResponse])
async def get_my_events(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(async_get_db)
):
    """
    Возвращает список мероприятий, в которых участвовал текущий пользователь.
    Связь ищется по email.
    """

    stmt = (
        select(Event)
        .join(Participant, Participant.event_id == Event.id)
        .where(Participant.email == current_user.email)
    )
    result = await db.execute(stmt)
    events = result.scalars().all()
    return events


@router.get("/events/{event_id}/info", response_model=EventDetailResponse)
async def get_event_info(
        event_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(async_get_db)
):
    """
    Возвращает информацию о хакатоне и роль/статус текущего пользователя в нем.
    """
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")

    p_stmt = select(Participant).where(
        Participant.event_id == event_id,
        Participant.email == current_user.email
    )
    p_result = await db.execute(p_stmt)
    participant = p_result.scalar_one_or_none()

    response = EventDetailResponse.model_validate(event)
    if participant:
        response.user_role = participant.role
        response.user_place = participant.place

    return response

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
    Скачать все сертификаты события одним ZIP-архивом.
    """
    try:
        service = CreateZipService(db)
        zip_buffer, filename = await service.get_user_zip(current_user)

        encoded_filename = quote(filename)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename*=utf-8''{encoded_filename}"
            }
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error downloading zip for event {current_user.username}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Не удалось скачать архив")
