import os

import pdfkit
from jinja2 import Template

# Настройка пути для сохранения
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_certificate_pdf(participant, event):
    """
    1. Берет HTML шаблон из Event.
    2. Подставляет данные Participant через Jinja2.
    3. Конвертирует в PDF.
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
    file_path = os.path.join(OUTPUT_DIR, filename)

    # Генерация PDF (простая конфигурация)
    # В продакшене лучше использовать WeasyPrint или headless chrome
    try:
        pdfkit.from_string(rendered_html, file_path)
        return file_path
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None


def send_email_mock(email: str, file_path: str):
    """
    Имитация отправки email.
    В реальности здесь будет код smtplib.
    """
    print(f"--- EMAIL SENT TO {email} with attachment {file_path} ---")
    return True
