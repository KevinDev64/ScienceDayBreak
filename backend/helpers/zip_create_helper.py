import io
import os
import zipfile

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.concurrency import run_in_threadpool

from core.config import logger
from database import Event, Participant


class CreateZipService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Убирает плохие символы из имени файла"""
        # Оставляем только буквы, цифры, пробел, тире и подчеркивание
        return "".join([c for c in name if c.isalnum() or c in (' ', '-', '_')]).strip()

    def _create_zip_sync(self, participants, event_name: str) -> io.BytesIO:
        """
        Синхронная функция создания архива.
        Запускается в отдельном потоке, чтобы не блокировать Event Loop.
        """
        zip_buffer = io.BytesIO()

        # Используем ZIP_DEFLATED для сжатия
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            files_added = 0

            for p in participants:
                # Проверяем, что путь есть в БД и файл физически существует
                if p.is_generated and p.file_path and os.path.exists(p.file_path):
                    # Формируем имя файла внутри архива: "Ivan_Ivanov_Student.pdf"
                    safe_name = self._sanitize_filename(p.name)
                    safe_role = self._sanitize_filename(p.role)
                    # Добавляем ID, чтобы избежать дубликатов имен файлов
                    archive_filename = f"{safe_name}_{safe_role}_{p.id}.pdf"

                    # write(путь_на_диске, имя_в_архиве)
                    zip_file.write(p.file_path, arcname=archive_filename)
                    files_added += 1

        if files_added == 0:
            # Это исключение будет перехвачено в run_in_threadpool
            raise ValueError("Нет доступных файлов для создания архива")

        zip_buffer.seek(0)
        return zip_buffer

    async def get_event_zip(self, event_id: int) -> tuple[io.BytesIO, str]:
        """
        Собирает архив всех сертификатов события.
        Возвращает (buffer, filename).
        """
        # 1. Получаем событие и участников
        # Используем selectinload не обязательно, если нам нужны просто поля Participant,
        # но нам нужно имя ивента. Проще сделать два запроса или join.

        event = await self.db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Событие не найдено")

        # Теперь участников с готовыми файлами
        result = await self.db.execute(
            select(Participant).where(
                Participant.event_id == event_id,
                Participant.is_generated == True,
                Participant.file_path.isnot(None)
            )
        )
        participants = result.scalars().all()

        if not participants:
            raise HTTPException(status_code=404, detail="Нет готовых сертификатов для этого события")

        return await self.create_event_zip(event.name, participants)

    async def get_user_zip(self, user) -> tuple[io.BytesIO, str]:
        """
        Собирает архив всех пользовательских сертификатов событий.
        Возвращает (buffer, filename).
        """

        stmt = (
            select(Participant)
            .join(Event, Participant.event_id == Event.id)  # Джойн нужен, чтобы получить имя ивента для названия файла
            .where(
                Participant.email == user.email,
                Participant.is_generated == True,
                Participant.file_path.isnot(None)
            )
        )
        stmt = stmt.options(selectinload(Participant.event))

        result = await self.db.execute(stmt)
        participants = result.scalars().all()

        if not participants:
            raise HTTPException(status_code=404, detail="Нет готовых сертификатов для скачивания")

        return await self.create_event_zip(user.username, participants)

    async def create_event_zip(self, name: str, participants: list[Participant]):
        try:
            zip_buffer = await run_in_threadpool(
                self._create_zip_sync,
                participants,
                name
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"ZIP Error: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при создании архива")

        # Формируем имя архива: "EventName_Certificates.zip"
        safe_event_name = self._sanitize_filename(name).replace(" ", "_")
        zip_filename = f"{safe_event_name}_Certificates.zip"

        return zip_buffer, zip_filename
