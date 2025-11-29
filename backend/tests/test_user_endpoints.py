import io
from unittest.mock import patch, AsyncMock

import pytest

from database import Event, Participant

MODULE_PATH = "api.routes.user"


@pytest.mark.asyncio
async def test_get_my_events(client, db_session, test_user, auth_headers):
    """Тест 1: Получение списка ивентов пользователя"""

    # 1. Создаем ивенты
    event1 = Event(id=1, name="Hackathon 1", date_str="01.12.2025", description="Hackathon 1", )
    event2 = Event(id=2, name="Hackathon 2", date_str="01.12.2025", description="Hackathon 1")
    db_session.add_all([event1, event2])

    # 2. Добавляем участие пользователя только в event1
    participant = Participant(
        event_id=1,
        email=test_user.email,
        role="Developer"
    )
    db_session.add(participant)
    await db_session.commit()

    # 3. Делаем запрос
    response = await client.get("api/v1/user/events", headers=auth_headers)

    # 4. Проверяем
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Hackathon 1"


@pytest.mark.asyncio
async def test_get_event_info_success(client, db_session, test_user, auth_headers):
    """Тест 2: Получение инфо об ивенте (участник существует)"""

    event = Event(id=10, name="Cool Event", date_str="2025-12-01", description="knknkn")
    db_session.add(event)

    part = Participant(
        event_id=10,
        email=test_user.email,
        role="Captain",
        place="1st"
    )
    db_session.add(part)
    await db_session.commit()

    response = await client.get("api/v1/user/events/10/info", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Cool Event"
    assert data["user_role"] == "Captain"
    assert data["user_place"] == "1st"


@pytest.mark.asyncio
async def test_get_event_info_not_participant(client, db_session, test_user, auth_headers):
    """Тест 2 (кейс 2): Получение инфо, если пользователь НЕ участник"""

    event = Event(id=20, name="Open Event", date_str="2025-12-01", description="Hackathon 1")
    db_session.add(event)
    await db_session.commit()

    response = await client.get("api/v1/user/events/20/info", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Open Event"
    # Поля роли должны быть пустыми (или None, в зависимости от вашей схемы)
    assert data.get("user_role") is None


@pytest.mark.asyncio
async def test_get_event_info_not_found(client, auth_headers):
    # ...
    response = await client.get("api/v1/user/events/999/info", headers=auth_headers)
    assert response.status_code == 404

    # 💥 ИСПРАВЛЕНО: ожидаем точное сообщение из вашего роутера
    assert response.json()["detail"] == "Мероприятие не найдено"


@pytest.mark.asyncio
async def test_download_certificate_success(client, db_session, test_user, auth_headers, tmp_path):
    """Тест 3: Успешное скачивание сертификата"""

    # Создаем временный файл
    cert_file = tmp_path / "cert_test.pdf"
    cert_file.write_bytes(b"%PDF-1.4 dummy content")

    event = Event(id=30,  date_str="2025-12-01", name="Cert Event", description="Cert Event", )
    db_session.add(event)

    part = Participant(
        event_id=30,
        email=test_user.email,
        is_generated=True,
        file_path=str(cert_file)
    )
    db_session.add(part)
    await db_session.commit()

    response = await client.get("api/v1/user/events/30/certificate", headers=auth_headers)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content == b"%PDF-1.4 dummy content"


@pytest.mark.asyncio
async def test_download_certificate_not_ready(client, db_session, test_user, auth_headers):
    """Тест 3 (кейс 2): Сертификат не готов"""

    event = Event(id=31,  date_str="2025-12-01", name="Cert Event", description="Cert Event")
    db_session.add(event)
    part = Participant(
        event_id=31,
        email=test_user.email,
        is_generated=False,
        file_path=None
    )
    db_session.add(part)
    await db_session.commit()

    response = await client.get("api/v1/user/events/31/certificate", headers=auth_headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Сертификат еще не готов"


@pytest.mark.asyncio
async def test_download_certificate_file_missing(client, db_session, test_user, auth_headers):
    """Тест 3 (кейс 3): В БД сказано готов, но файла нет на диске"""

    event = Event(id=32)
    db_session.add(event)
    part = Participant(
        event_id=32,
        email=test_user.email,
        is_generated=True,
        file_path="/path/to/non/existent/file.pdf"
    )
    db_session.add(part)
    await db_session.commit()

    response = await client.get("api/v1/user/events/32/certificate", headers=auth_headers)

    assert response.status_code == 500
    assert "не найден на сервере" in response.json()["detail"]


@pytest.mark.asyncio
async def test_download_certificate_not_participant(client, db_session, test_user, auth_headers):
    """Тест 3 (кейс 4): Пользователь не участвовал"""
    event = Event(id=33)
    db_session.add(event)
    await db_session.commit()

    response = await client.get("api/v1/user/events/33/certificate", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Вы не являетесь участником этого события"


@pytest.mark.asyncio
async def test_download_all_certificates_zip(client, auth_headers):
    """
    Тест 4: Скачивание ZIP архива.
    Мы мокаем CreateZipService, чтобы не тестировать создание zip-файла, 
    а только логику endpoint-а.
    """
    # Патчим класс CreateZipService там, где он импортируется в роутере
    with patch(f"{MODULE_PATH}.CreateZipService") as MockServiceClass:
        # Настраиваем мок
        mock_service_instance = MockServiceClass.return_value

        # Имитируем возвращение буфера и имени файла
        dummy_zip = io.BytesIO(b"PK\x03\x04 dummy zip content")
        mock_service_instance.get_user_zip = AsyncMock(return_value=(dummy_zip, "certificates.zip"))

        response = await client.get("api/v1/user/my-certificates/download-all", headers=auth_headers)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"
        # Проверяем, что filename закодирован (RFC 5987)
        assert "filename*=utf-8''certificates.zip" in response.headers["content-disposition"]
        assert response.content == b"PK\x03\x04 dummy zip content"

        # Проверяем, что сервис был вызван
        MockServiceClass.assert_called_once()
        mock_service_instance.get_user_zip.assert_called_once()


@pytest.mark.asyncio
async def test_download_all_certificates_error(client, auth_headers):
    """Тест 4 (кейс 2): Ошибка при генерации архива"""

    with patch(f"{MODULE_PATH}.CreateZipService") as MockServiceClass:
        mock_service_instance = MockServiceClass.return_value
        # Имитируем исключение
        mock_service_instance.get_user_zip = AsyncMock(side_effect=Exception("Something went wrong"))

        response = await client.get("api/v1/user/my-certificates/download-all", headers=auth_headers)

        assert response.status_code == 500
        assert response.json()["detail"] == "Не удалось скачать архив"
