import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from core.config import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Генерируем уникальный ID для каждого запроса
        request_id = str(uuid.uuid4())

        # Добавляем ID в заголовки, чтобы его можно было проследить
        # и на клиенте, и в других сервисах.
        request.state.request_id = request_id

        # Собираем основную информацию о запросе
        logging_dict = {
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_host": request.client.host,
            "client_port": request.client.port,
        }

        start_time = time.time()

        response = None
        try:
            response = await call_next(request)
            # После выполнения запроса добавляем в лог статус-код ответа
            logging_dict["status_code"] = response.status_code
        except Exception as e:
            # В случае исключения логируем с уровнем ERROR
            logging_dict["status_code"] = 500
            logger.error(
                "Unhandled exception",
                extra={
                    "log_type": "request_log",
                    "request_id": request_id,
                    "request_details": logging_dict,
                },
                exc_info=e  # Добавляем информацию об исключении
            )
            # Важно! Передаем исключение дальше, чтобы FastAPI мог
            # сформировать корректный 500-ответ.
            raise e
        finally:
            process_time = (time.time() - start_time) * 1000  # в миллисекундах
            logging_dict["process_time_ms"] = round(process_time)

            # Логируем всю собранную информацию одной записью
            logger.info(
                "Request processed",
                extra={
                    "log_type": "request_log",
                    "request_id": request_id,
                    "request_details": logging_dict
                }
            )

            # Добавляем ID запроса в заголовок ответа
            if response:
                response.headers["X-Request-ID"] = request_id

            return response
