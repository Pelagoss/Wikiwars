#!/bin/sh

if [ "$DATABASE" = "wikiwars" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    python manage.py --app=manage:app db upgrade

    echo "PostgreSQL started"
fi

exec "$@"