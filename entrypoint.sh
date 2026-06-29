#!/bin/sh

echo "Waiting for postgres..."
until pg_isready -h db -U postgres; do
  sleep 2
done
echo "Postgres is ready."

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading initial data..."
python manage.py loaddata data.json 2>/dev/null || true

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
