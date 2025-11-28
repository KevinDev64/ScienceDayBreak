import os

from jinja2 import Template
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from core.config import OUTPUT_DIR


# Настройка пути для сохранения


async def generate_certificate_pdf(participant, event):
    """
    1. Берет HTML шаблон из Event.
    2. Подставляет данные Participant через Jinja2.
    3. Конвертирует в PDF с помощью WeasyPrint.
    """
    # Рендеринг HTML
    template = Template(event.template_html)
    rendered_html = template.render(
        name=participant.name,
        role=participant.role,
        event_name=event.name,
        date=event.date_str,
        place=participant.place or ""
    )

    # Имя файла
    filename = f"{event.id}_{participant.id}_cert.pdf"
    file_path = os.path.join(OUTPUT_DIR, str(event.id), filename)

    # Генерация PDF с WeasyPrint
    try:
        # Конфигурация шрифтов (опционально)
        font_config = FontConfiguration()

        # Создание HTML объекта
        html = HTML(string=rendered_html)

        # Создаем CSS стили правильно
        css_string = """
        @page {
            size: A4 landscape;
            margin: 2cm;
        }
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        """

        # Генерация PDF
        html.write_pdf(
            file_path,
            font_config=font_config,
            stylesheets=[CSS(string=css_string)]  # Используем CSS класс
        )

        print(f"PDF успешно сгенерирован: {file_path}")
        return file_path

    except Exception as e:
        print(f"Error generating PDF with WeasyPrint: {e}")
        return None


async def send_email_mock(email: str, file_path: str):
    """
    Имитация отправки email.
    В реальности здесь будет код smtplib.
    """
    print(f"--- EMAIL SENT TO {email} with attachment {file_path} ---")
    return True