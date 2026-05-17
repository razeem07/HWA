#!/bin/sh

# Wait for database to be ready (optional but recommended)
echo "Waiting for postgres..."

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute the CMD from Dockerfile (this starts Gunicorn)
exec "$@"