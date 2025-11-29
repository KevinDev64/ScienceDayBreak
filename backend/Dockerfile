FROM python:3.11-alpine

WORKDIR /app

RUN apk update
RUN apk upgrade

RUN apk add weasyprint

RUN pip3 install --upgrade pip

COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY . .

COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

#ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["/bin/sh", "-c", "python3 main.py"]
