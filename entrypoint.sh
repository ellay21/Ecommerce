#!/bin/sh

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:$PORT --workers 4