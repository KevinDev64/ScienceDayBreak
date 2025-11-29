import os

from sqlalchemy import select

import worker
from core.config import async_get_db, OUTPUT_DIR
from database import Event, Participant
from mail.service import send_email_real


async def background_worker_async(event_id: int):
    """Асинхронная фоновая задача"""
    async for db in async_get_db():
        try:
            # Получаем свежие данные внутри задачи
            event = await db.get(Event, event_id)
            if not event:
                return

            result = await db.execute(
                select(Participant).filter(
                    Participant.event_id == event_id,
                    Participant.is_sent == False
                )
            )
            participants = result.scalars().all()
            if participants:
                os.makedirs(f"{OUTPUT_DIR}/{event_id}", exist_ok=True)

            for p in participants:
                # 1. Генерация
                path = await worker.generate_certificate_pdf(p, event)
                if path:
                    p.file_path = path
                    p.is_generated = True

                    # sent = await send_email_real(p.email,
                    #                              p.file_path,
                    #                              event.name,
                    #                              event.description,
                    #                              event.date_str)
                    # # 2. Отправка
                    sent = await worker.send_email_mock(p.email, path)
                    if sent:
                        p.is_sent = True

                    await db.commit()

        except Exception as e:
            print(f"Error in background task: {e}")


