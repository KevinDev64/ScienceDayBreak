#!/bin/sh
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

echo "Applying database migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"