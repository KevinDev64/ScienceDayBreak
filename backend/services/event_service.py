import io
import math
import os
import uuid

import aiofiles
import pandas as pd
from fastapi import UploadFile, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import logger
from core.templates import default_template
from database import Event, Participant


class EventService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _safe_str(value):
        """Безопасное преобразование в строку с проверкой на NaN для float"""
        if value is None:
            return ''
        # Исправленный баг: math.isnan падает на строках
        if isinstance(value, float) and math.isnan(value):
            return ''
        return str(value).strip()

    async def save_image(self, file: UploadFile) -> str | None:
        """Сохраняет изображение и возвращает путь"""
        if not file:
            return None

        try:
            os.makedirs("data", exist_ok=True)

            # Безопасное получение расширения
            filename_orig = file.filename or "image.png"
            extension = os.path.splitext(filename_orig)[1]
            if not extension:
                extension = ".png"

            new_filename = f"event_{uuid.uuid4().hex}{extension}"
            file_path = os.path.join("data", new_filename)

            async with aiofiles.open(file_path, "wb") as out_file:
                while content := await file.read(1024 * 1024):  # Читаем по 1Мб
                    await out_file.write(content)

            logger.info(f"📸 Картинка сохранена: {file_path}")
            # Возвращаем путь с прямыми слешами для унификации в БД
            return file_path.replace("\\", "/")

        except Exception as e:
            logger.error(f"Ошибка при сохранении файла: {e}")
            raise HTTPException(status_code=500, detail="Не удалось сохранить изображение")

    async def parse_and_save_csv(self, event_id: int, file_content: bytes) -> int:
        """Парсит CSV и сохраняет участников. Возвращает количество добавленных."""
        try:
            # Используем BytesIO для pandas
            df = pd.read_csv(io.BytesIO(file_content))
        except Exception as e:
            logger.error(f"Ошибка чтения CSV: {e}")
            raise HTTPException(status_code=400, detail="Некорректный формат CSV файла")

        required_cols = ['name', 'email', 'role']
        if not all(col in df.columns for col in required_cols):
            raise HTTPException(
                status_code=400,
                detail=f"CSV должен содержать колонки: {', '.join(required_cols)}"
            )

        count = 0
        for _, row in df.iterrows():
            participant = Participant(
                event_id=event_id,
                name=self._safe_str(row['name']),
                email=self._safe_str(row['email']),
                role=self._safe_str(row['role']),
                place=self._safe_str(row.get('place', ''))
            )
            self.db.add(participant)
            count += 1

        await self.db.commit()
        return count

    async def create_event(self, event_data, image_file: UploadFile | None, csv_file: UploadFile | None):
        image_path = await self.save_image(image_file)

        new_event = Event(
            name=event_data.name,
            date_str=event_data.date_str,
            template_html=default_template,
            description=event_data.description,
            image_path=image_path,
        )

        self.db.add(new_event)
        await self.db.commit()
        await self.db.refresh(new_event)

        uploaded_count = 0
        if csv_file:
            content = await csv_file.read()
            uploaded_count = await self.parse_and_save_csv(new_event.id, content)
            logger.info(f"📄 Загружен CSV для нового события {new_event.id}: {uploaded_count} участников")

        return new_event, uploaded_count

    async def update_event(self, event_id: int, event_data, image_file: UploadFile | None, csv_file: UploadFile | None):
        query = select(Event).where(Event.id == event_id)
        result = await self.db.execute(query)
        event = result.scalar_one_or_none()

        if not event:
            raise HTTPException(status_code=404, detail="Событие не найдено")

        # Обновляем поля
        if event_data.name is not None: event.name = event_data.name
        if event_data.date_str is not None: event.date_str = event_data.date_str
        if event_data.description is not None: event.description = event_data.description

        if image_file:
            event.image_path = await self.save_image(image_file)

        uploaded_count = 0
        if csv_file:
            content = await csv_file.read()
            uploaded_count = await self.parse_and_save_csv(event_id, content)

        await self.db.commit()
        await self.db.refresh(event)

        return event, uploaded_count

    async def get_participants_with_links(self, event_id: int, request: Request):
        query = select(Participant).where(Participant.event_id == event_id)
        result = await self.db.execute(query)
        participants = result.scalars().all()

        response_list = []
        for p in participants:
            download_link = None
            if p.is_generated and p.file_path:
                # Убираем начальные слеши и создаем валидный URL
                clean_path = p.file_path.replace("\\", "/").lstrip("/")
                download_link = str(request.base_url.replace(path=f"static/{clean_path}"))

            p_dict = {
                "id": p.id,
                "event_id": p.event_id,
                "name": p.name,
                "email": p.email,
                "role": p.role,
                "place": p.place,
                "is_generated": p.is_generated,
                "is_sent": p.is_sent,
                "download_url": download_link
            }
            response_list.append(p_dict)

        return response_list

    async def check_unsent_participants(self, event_id: int) -> bool:
        """Проверяет, есть ли участники, которым еще не отправлено/сгенерировано"""
        result = await self.db.execute(
            select(Participant).filter(
                Participant.event_id == event_id,
                Participant.is_sent == False
            ).limit(1)
        )
        return result.scalar() is not None
