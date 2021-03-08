#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py makemigrations
python3 manage.py migrate

# DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME \
# DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD \
# DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL \
# python3 manage.py createsuperuser --noinput
cd wantem
ls -l
cd pattern
ls -l 
cd pattern 
ls -l
cd /workspace

celery -A config worker --detach
gunicorn config.wsgi --bind=0.0.0.0:8000
