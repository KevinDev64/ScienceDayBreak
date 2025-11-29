import aiosmtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from jinja2 import Template

from core.config import SMTP_FROM_NAME, SMTP_USER, SMTP_HOST, SMTP_PORT, SMTP_PASSWORD, logger


async def send_email_real(
        email: str,
        file_path: str,
        event_title: str = None,
        event_description: str = None,
        event_date: str = None
):
    """
    Отправка email с HTML шаблоном.
    """
    try:

        if not os.path.exists(file_path):
            logger.log(f"❌ Файл не найден: {file_path}")
            return False

        file_name = os.path.basename(file_path)
        file_size = round(os.path.getsize(file_path) / 1024, 1)
        file_extension = file_name.split('.')[-1].upper()

        template_path = Path("templates/email_template.html")
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        template = Template(template_content)
        html_content = template.render(
            event_title=event_title,
            event_description=event_description,
            event_date=event_date,
            file_name=file_name,
            file_size=file_size,
            file_type=file_extension
        )

        message = MIMEMultipart("alternative")
        message["From"] = f"{SMTP_FROM_NAME} <{SMTP_USER}>"
        message["To"] = email
        message["Subject"] = event_title or "Новое событие"

        text_content = f"""
Новое событие!

Информация о событии:
Название: {event_title or 'Не указано'}
Описание: {event_description or 'Не указано'}
Дата: {event_date or 'Не указана'}

Это письмо было отправлено автоматически.
        """

        message.attach(MIMEText(text_content, "plain"))
        message.attach(MIMEText(html_content, "html"))

        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={file_name}",
        )
        message.attach(part)

        logger.log(f"🔄 Отправка email на {email}...")

        async with aiosmtplib.SMTP(hostname=SMTP_HOST, port=SMTP_PORT) as smtp:
            await smtp.starttls()
            await smtp.login(SMTP_USER, SMTP_PASSWORD)
            await smtp.send_message(message)

        logger.log(f"✅ Email успешно отправлен на {email}")
        logger.log(f"📎 Прикрепленный файл: {file_name} ({file_size} KB)")

        return True

    except Exception as e:
        logger.error(f"❌ Ошибка отправки email: {e}", exc_info=True)
        return False