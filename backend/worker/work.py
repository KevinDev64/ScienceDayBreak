import os

from jinja2 import Template
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from core import templates
from core.config import OUTPUT_DIR, logger


async def generate_certificate_pdf(participant, event):
    """
    1. Берет HTML шаблон из Event.
    2. Подставляет данные Participant через Jinja2.
    3. Конвертирует в PDF с помощью WeasyPrint.
    """

    template = Template(templates.templates[event.template_html])
    rendered_html = template.render(
        name=participant.name,
        role=participant.role,
        event_name=event.name,
        date=event.date_str,
        place=participant.place or ""
    )
    logger.info("Начато создание")


    filename = f"{event.id}_{participant.id}_cert.pdf"
    file_path = os.path.join(OUTPUT_DIR, str(event.id), filename)

    try:
        font_config = FontConfiguration()

        html = HTML(string=rendered_html)

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

        html.write_pdf(
            file_path,
            font_config=font_config,
            stylesheets=[CSS(string=css_string)]
        )

        logger.info(f"PDF успешно сгенерирован: {file_path}")
        return file_path

    except Exception as e:
        logger.error("Error generating PDF with WeasyPrint: {e}")
        return None
