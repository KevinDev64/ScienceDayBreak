
from typing import List
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import async_get_db, logger
from helpers import background_worker_async
from schemas import EventCreateForm, EventUpdateForm
from schemas.response import ParticipantResponse
from services import EventService
from helpers import CreateZipService

router = APIRouter(prefix="/operator", tags=["Endpoints for operator"])


def schedule_background_work(event_id: int, background_tasks: BackgroundTasks):
    """
    Планирует задачу, только если передан ID.
    Важно: background_worker_async должен создавать свою сессию БД,
    а не использовать сессию из dependency, которая закроется.
    """
    background_tasks.add_task(background_worker_async, event_id)


@router.post("/event")
async def create_event(
        background_tasks: BackgroundTasks,
        event_data: EventCreateForm = Depends(),
        db: AsyncSession = Depends(async_get_db),
):
    try:
        service = EventService(db)

        new_event, participants_count = await service.create_event(
            event_data=event_data,
            image_file=event_data.image,
            csv_file=event_data.csv_file
        )

        if participants_count > 0:
            schedule_background_work(new_event.id, background_tasks)

        return {
            "status": "success",
            "event_id": new_event.id,
            "message": f"Событие создано. Участников загружено: {participants_count}",
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating event: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при создании события"
        )


@router.put("/event/{event_id}")
async def update_event(
        event_id: int,
        background_tasks: BackgroundTasks,
        event_data: EventUpdateForm = Depends(),
        db: AsyncSession = Depends(async_get_db)
):
    try:
        service = EventService(db)
        event, participants_count = await service.update_event(
            event_id=event_id,
            event_data=event_data,
            image_file=event_data.image,
            csv_file=event_data.csv_file
        )

        if participants_count > 0:
            schedule_background_work(event.id, background_tasks)

        return {
            "status": "success",
            "event_id": event.id,
            "message": "Событие обновлено",
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating event {event_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Не удалось обновить событие")


@router.get("/event/{event_id}/participants", response_model=List[ParticipantResponse])
async def get_event_participants(
        event_id: int,
        request: Request,
        db: AsyncSession = Depends(async_get_db)
):
    try:
        service = EventService(db)
        participants_data = await service.get_participants_with_links(event_id, request)
        return participants_data

    except Exception as e:
        logger.error(f"Error fetching participants for {event_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка при получении списка участников")


@router.post("/events/{event_id}/upload-csv")
async def upload_participants(
        event_id: int,
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(async_get_db)):
    """
       Отдельная ручка для дозагрузки CSV
    """
    try:
        service = EventService(db)
        content = await file.read()

        count = await service.parse_and_save_csv(event_id, content)

        if count > 0:
            schedule_background_work(event_id, background_tasks)

        return {"message": f"Загружено {count} участников. Генерация запущена в фоне."}

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error uploading CSV for {event_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка при обработке файла")


@router.get("/event/{event_id}/download-all")
async def download_all_certificates_zip(
        event_id: int,
        # Если нужно ограничить доступ только для создателя или админа, добавьте current_user сюда
        db: AsyncSession = Depends(async_get_db)
):
    """
    Скачать все сертификаты события одним ZIP-архивом.
    """
    try:
        service = CreateZipService(db)
        zip_buffer, filename = await service.get_event_zip(event_id)

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
        logger.error(f"Error downloading zip for event {event_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Не удалось скачать архив")