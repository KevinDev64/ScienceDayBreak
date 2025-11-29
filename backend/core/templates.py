
default_template = """
    <html>
    <body style="border: 10px solid #333; padding: 20px; text-align: center;">
        <h1>СЕРТИФИКАТ</h1>
        <h3>Вручается</h3>
        <h2>{{ name }}</h2>
        <p>За участие в мероприятии: <b>{{ event_name }}</b></p>
        <p>Роль: {{ role }}</p>
        <p>Дата: {{ date }}</p>
    </body>
    </html>
    """

templates = {1: default_template}