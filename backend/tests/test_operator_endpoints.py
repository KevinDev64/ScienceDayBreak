from io import BytesIO
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from fastapi import status

MODULE_PATH = "api.routes.operator"

# --- Мокируемые данные ---

MOCK_EVENT = MagicMock(id=101, name="Mock Event")
MOCK_EVENT_ID = MOCK_EVENT.id


MOCK_PARTICIPANTS = [
    {
        "id": 1,
        "name": "User 1",
        "download_url": "http://test/static/cert1.pdf",
        "event_id": 1,  # ← Добавьте недостающие поля
        "email": "user1@example.com",
        "role": "participant",
        "is_generated": True,
        "is_sent": False
    },
    {
        "id": 2,
        "name": "User 2",
        "download_url": None,
        "event_id": 1,  # ← Добавьте недостающие поля
        "email": "user2@example.com",
        "role": "participant",
        "is_generated": False,
        "is_sent": False
    }
]

MOCK_CSV_CONTENT = b"name,email,role\nTest,test@example.com,member"
MOCK_IMAGE_CONTENT = b"image content"


from io import BytesIO
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from fastapi import status, HTTPException

MODULE_PATH = "api.routes.operator"

# --- Мокируемые данные ---

MOCK_EVENT = MagicMock(id=101, name="Mock Event")
MOCK_EVENT_ID = MOCK_EVENT.id

MOCK_EVENTS_LIST = [
    {"id": 1, "name": "Event 1", "date_str": "2025-01-01"},
    {"id": 2, "name": "Event 2", "date_str": "2025-02-01"}
]

MOCK_PARTICIPANTS = [
    {
        "id": 1,
        "name": "User 1",
        "download_url": "http://test/static/cert1.pdf",
        "event_id": 1,
        "email": "user1@example.com",
        "role": "participant",
        "is_generated": True,
        "is_sent": False
    },
    {
        "id": 2,
        "name": "User 2",
        "download_url": None,
        "event_id": 1,
        "email": "user2@example.com",
        "role": "participant",
        "is_generated": False,
        "is_sent": False
    }
]
#
# MOCK_CSV_CONTENT = b"name,email,role\nTest,test@example.com,member"
# MOCK_IMAGE_CONTENT = b"image content"
#
#
# # --- Фикстуры для Mock-объектов ---
#
# @pytest.fixture
# def mock_current_user():
#     """Мок текущего пользователя (оператора)."""
#     mock_user = MagicMock()
#     mock_user.id = 1
#     mock_user.email = "operator@example.com"
#     mock_user.role = "operator"
#     return mock_user
#
#
# @pytest.fixture(autouse=True)
# def mock_auth_dependency(mock_current_user):
#     """Автоматически мокаем зависимость аутентификации для всех тестов."""
#     with patch(f"{MODULE_PATH}.require_operator", return_value=mock_current_user) as mock_auth:
#         yield mock_auth
#
#
# @pytest.fixture
# def mock_zip_service():
#     """Мок CreateZipService."""
#     with patch(f"{MODULE_PATH}.CreateZipService") as MockZipServiceClass:
#         mock_instance = MockZipServiceClass.return_value
#         mock_instance.get_event_zip = AsyncMock(
#             return_value=(
#                 BytesIO(b"zip_content"),
#                 f"certificates_{MOCK_EVENT_ID}.zip"
#             )
#         )
#         yield MockZipServiceClass
#
#
# @pytest.fixture
# def mock_event_service():
#     """Мок EventService для всех роутов, требующих его."""
#     with patch(f"{MODULE_PATH}.EventService") as MockEventServiceClass:
#         mock_instance = MockEventServiceClass.return_value
#         yield mock_instance
#
#
# @pytest.fixture
# def mock_background_worker():
#     """Мок фонового обработчика."""
#     with patch(f"{MODULE_PATH}.background_worker_async", new=AsyncMock()) as mock_worker:
#         yield mock_worker
#
#
# # =================================================================
# # 0. GET MY CREATED EVENTS (GET /events)
# # =================================================================
#
# @pytest.mark.asyncio
# async def test_get_my_created_events_success(client, mock_event_service, mock_current_user):
#     """Успешное получение списка событий, созданных текущим пользователем."""
#
#     mock_event_service.get_events_by_creator = AsyncMock(return_value=MOCK_EVENTS_LIST)
#
#     response = await client.get("/api/v1/operator/events")
#
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == MOCK_EVENTS_LIST
#     mock_event_service.get_events_by_creator.assert_called_once_with(mock_current_user.id)
#
#
# @pytest.mark.asyncio
# async def test_get_my_created_events_unauthorized(client):
#     """Тест на отсутствие авторизации."""
#
#     with patch(f"{MODULE_PATH}.require_operator", side_effect=HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#     )):
#         response = await client.get("/api/v1/operator/events")
#
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#
# @pytest.mark.asyncio
# async def test_get_my_created_events_internal_error(client, mock_event_service):
#     """Тест на внутреннюю ошибку при получении списка событий."""
#
#     mock_event_service.get_events_by_creator = AsyncMock(side_effect=Exception("Database error"))
#
#     response = await client.get("/api/v1/operator/events")
#
#     assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#     assert "Ошибка при получении списка событий" in response.json()["detail"]
#
#
# # =================================================================
# # 1. CREATE EVENT (POST /event)
# # =================================================================
#
# @pytest.mark.asyncio
# async def test_create_event_success_no_participants(client, mock_event_service, mock_background_worker, mock_current_user):
#     """Успешное создание события без участников (без CSV)."""
#
#     mock_event_service.create_event = AsyncMock(return_value=(MOCK_EVENT, 0))
#
#     response = await client.post(
#         "/api/v1/operator/event",
#         data={
#             "name": "New Event",
#             "date_str": "2025-01-01",
#             "description": "Desc"
#         }
#     )
#
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["event_id"] == MOCK_EVENT_ID
#     assert response.json()["status"] == "success"
#     mock_event_service.create_event.assert_called_once()
#     call_args = mock_event_service.create_event.call_args
#     assert call_args.kwargs['user_id'] == mock_current_user.id
#     mock_background_worker.assert_not_called()
#
#
# @pytest.mark.asyncio
# async def test_create_event_success_with_participants(client, mock_event_service, mock_background_worker, mock_current_user):
#     """Успешное создание события c участниками (с CSV)."""
#
#     mock_event_service.create_event = AsyncMock(return_value=(MOCK_EVENT, 5))
#
#     response = await client.post(
#         "/api/v1/operator/event",
#         data={
#             "name": "New Event",
#             "date_str": "2025-01-01",
#             "description": "Desc"
#         },
#         files={
#             "csv_file": ("data.csv", MOCK_CSV_CONTENT, "text/csv")
#         }
#     )
#
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["event_id"] == MOCK_EVENT_ID
#     mock_event_service.create_event.assert_called_once()
#     call_args = mock_event_service.create_event.call_args
#     assert call_args.kwargs['user_id'] == mock_current_user.id
#     mock_background_worker.assert_called_once_with(MOCK_EVENT_ID)
#
#
# @pytest.mark.asyncio
# async def test_create_event_unauthorized(client):
#     """Попытка создания события без авторизации."""
#
#     with patch(f"{MODULE_PATH}.require_operator", side_effect=HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#     )):
#         response = await client.post(
#             "/api/v1/operator/event",
#             data={
#                 "name": "New Event",
#                 "date_str": "2025-01-01",
#                 "description": "Desc"
#             }
#         )
#
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#
# @pytest.mark.asyncio
# async def test_create_event_internal_error(client, mock_event_service):
#     """Тест на внутреннюю ошибку EventService."""
#
#     mock_event_service.create_event = AsyncMock(side_effect=Exception("DB connection failure"))
#
#     response = await client.post(
#         "/api/v1/operator/event",
#         data={
#             "name": "New Event",
#             "date_str": "2025-01-01",
#             "description": "Desc"
#         }
#     )
#
#     assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#     assert "Внутренняя ошибка сервера" in response.json()["detail"]


# Остальные тесты остаются аналогично обновленными...
# [Аналогично обновите тесты для UPDATE, GET PARTICIPANTS, UPLOAD CSV, DOWNLOAD ZIP]

#
#
# @pytest.fixture
# def mock_zip_service():
#     """Мок CreateZipService."""
#     with patch(f"{MODULE_PATH}.CreateZipService") as MockZipServiceClass:
#         mock_instance = MockZipServiceClass.return_value
#         # Настройка get_event_zip для возврата фиктивных данных ZIP
#         mock_instance.get_event_zip = AsyncMock(
#             return_value=(
#                 BytesIO(b"zip_content"),
#                 f"certificates_{MOCK_EVENT_ID}.zip"
#             )
#         )
#         yield MockZipServiceClass
#
#
# @pytest.fixture
# def mock_event_service():
#     """Мок EventService для всех роутов, требующих его."""
#     with patch(f"{MODULE_PATH}.EventService") as MockEventServiceClass:
#         mock_instance = MockEventServiceClass.return_value
#         yield mock_instance
#
#
# @pytest.fixture
# def mock_background_worker():
#     """Мок фонового обработчика."""
#     with patch(f"{MODULE_PATH}.background_worker_async", new=AsyncMock()) as mock_worker:
#         yield mock_worker
#
#
# # =================================================================
# # 1. CREATE EVENT (POST /event)
# # =================================================================
#
# @pytest.mark.asyncio
# async def test_create_event_success_no_participants(client, mock_event_service, mock_background_worker):
#     """Успешное создание события без участников (без CSV)."""
#
#     # Настройка мока: событие создано, 0 участников
#     mock_event_service.create_event = AsyncMock(return_value=(MOCK_EVENT, 0))
#
#     response = await client.post(
#         "api/v1/operator/event",
#         data={
#             "name": "New Event",
#             "date_str": "2025-01-01",
#             "description": "Desc"
#         }
#     )
#
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["event_id"] == MOCK_EVENT_ID
#     # Проверяем, что фоновая задача НЕ была запланирована
#     mock_background_worker.assert_not_called()
#

# @pytest.mark.asyncio
# async def test_create_event_success_with_participants(client, mock_event_service, mock_background_worker):
#     """Успешное создание события c участниками (с CSV)."""
#
#     # Настройка мока: событие создано, 5 участников
#     mock_event_service.create_event = AsyncMock(return_value=(MOCK_EVENT, 5))
#
#     response = await client.post(
#         "api/v1/operator/event",
#         data={
#             "name": "New Event",
#             "date_str": "2025-01-01",
#             "description": "Desc"
#         },
#         files={
#             "csv_file": ("data.csv", MOCK_CSV_CONTENT, "text/csv")
#         }
#     )
#
#     assert response.status_code == status.HTTP_200_OK
#     # Проверяем, что фоновая задача была запланирована
#     mock_background_worker.assert_called_once_with(MOCK_EVENT_ID)
#
#
# @pytest.mark.asyncio
# async def test_create_event_internal_error(client, mock_event_service):
#     """Тест на внутреннюю ошибку EventService."""
#
#     # Настройка мока: EventService.create_event вызывает исключение
#     mock_event_service.create_event = AsyncMock(side_effect=Exception("DB connection failure"))
#
#     response = await client.post(
#         "api/v1/operator/event",
#         data={
#             "name": "New Event",
#             "date_str": "2025-01-01",
#             "description": "Desc"
#         }
#     )
#
#     assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#     assert "Внутренняя ошибка сервера" in response.json()["detail"]
#
#
# # =================================================================
# # 2. UPDATE EVENT (PUT /event/{event_id})
# # =================================================================
#
# @pytest.mark.asyncio
# async def test_update_event_success(client, mock_event_service, mock_background_worker):
#     """Успешное обновление события с загрузкой новых участников."""
#
#     # Настройка мока: событие обновлено, 3 новых участника
#     mock_event_service.update_event = AsyncMock(return_value=(MOCK_EVENT, 3))
#
#     response = await client.put(
#         f"api/v1/operator/event/{MOCK_EVENT_ID}",
#         data={
#             "name": "Updated Name",
#             "date_str": "2026-01-01"
#         },
#         files={
#             "csv_file": ("new_data.csv", MOCK_CSV_CONTENT, "text/csv")
#         }
#     )
#
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["event_id"] == MOCK_EVENT_ID
#     # Проверяем, что фоновая задача была запланирована
#     mock_background_worker.assert_called_once_with(MOCK_EVENT_ID)
#
#
# # test_operator_endpoints.py (продолжение)
#
# # =================================================================
# # 3. GET PARTICIPANTS (GET /event/{event_id}/participants)
# # =================================================================
#
# @pytest.mark.asyncio
# async def test_get_event_participants_success(client, mock_event_service):
#     """Успешное получение списка участников сгенерированного события."""
#
#     # Настройка мока
#     mock_event_service.get_participants_with_links = AsyncMock(return_value=MOCK_PARTICIPANTS)
#
#     response = await client.get(f"/api/v1/operator/event/{MOCK_EVENT_ID}/participants")
#
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) == 2
#     assert response.json()[0]["download_url"].startswith("http://test/")
#
#
# @pytest.mark.asyncio
# async def test_get_event_participants_internal_error(client, mock_event_service):
#     """Тест на внутреннюю ошибку при получении списка."""
#
#     mock_event_service.get_participants_with_links = AsyncMock(side_effect=Exception("Database error"))
#
#     response = await client.get(f"/api/v1/operator/event/{MOCK_EVENT_ID}/participants")
#
#     assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#     assert "Ошибка при получении списка участников" in response.json()["detail"]
#
#
# # =================================================================
# # 4. UPLOAD CSV (POST /events/{event_id}/upload-csv)
# # =================================================================
#
# @pytest.mark.asyncio
# async def test_upload_participants_success(client, mock_event_service, mock_background_worker):
#     """Успешная дозагрузка CSV и запуск фона."""
#
#     # Настройка мока: 10 новых участников
#     mock_event_service.parse_and_save_csv = AsyncMock(return_value=10)
#
#     response = await client.post(
#         f"api/v1/operator/events/{MOCK_EVENT_ID}/upload-csv",
#         files={"file": ("participants.csv", MOCK_CSV_CONTENT, "text/csv")}
#     )
#
#     assert response.status_code == status.HTTP_200_OK
#     assert "Загружено 10 участников" in response.json()["message"]
#     mock_event_service.parse_and_save_csv.assert_called_once()
#     # Фоновая задача должна быть запланирована, т.к. count > 0
#     mock_background_worker.assert_called_once_with(MOCK_EVENT_ID)
#
#
# @pytest.mark.asyncio
# async def test_upload_participants_no_background_task(client, mock_event_service, mock_background_worker):
#     """Загрузка CSV с 0 участниками не запускает фоновую задачу."""
#
#     # Настройка мока: 0 участников
#     mock_event_service.parse_and_save_csv = AsyncMock(return_value=0)
#
#     response = await client.post(
#         f"api/v1/operator/events/{MOCK_EVENT_ID}/upload-csv",
#         files={"file": ("participants.csv", MOCK_CSV_CONTENT, "text/csv")}
#     )
#
#     assert response.status_code == status.HTTP_200_OK
#     assert "Загружено 0 участников" in response.json()["message"]
#     # Проверяем, что фоновая задача НЕ была запланирована
#     mock_background_worker.assert_not_called()
#
#
# # test_operator_endpoints.py (продолжение)
#
# # =================================================================
# # 5. DOWNLOAD ZIP (GET /event/{event_id}/download-all)
# # =================================================================
#
# @pytest.mark.asyncio
# async def test_download_all_certificates_success(client, mock_zip_service):
#     """Успешное скачивание ZIP-архива."""
#
#     response = await client.get(f"/api/v1/operator/event/{MOCK_EVENT_ID}/download-all")
#
#     assert response.status_code == status.HTTP_200_OK
#     assert response.headers["content-type"] == "application/zip"
#     assert "attachment" in response.headers["content-disposition"]
#     assert response.content == b"zip_content"
#
#     # Проверяем, что CreateZipService был вызван
#     mock_zip_service.return_value.get_event_zip.assert_called_once_with(MOCK_EVENT_ID)
#
#
# @pytest.mark.asyncio
# async def test_download_all_certificates_internal_error(client, mock_zip_service):
#     """Обработка внутренней ошибки при скачивании."""
#
#     # Настройка мока: get_event_zip вызывает исключение
#     mock_zip_service.return_value.get_event_zip = AsyncMock(side_effect=Exception("File system error"))
#
#     response = await client.get(f"api/v1/operator/event/{MOCK_EVENT_ID}/download-all")
#
#     assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#     assert "Не удалось скачать архив" in response.json()["detail"]
