#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

rm -f ./*.pid

printf "Checking PostgreSQL availability...\n"
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -q
do
  printf "Database unavailable, waiting 1 second...\n"
  sleep 1;
done
printf "Database available!\n"

python manage.py makemigrations
python manage.py migrate
python manage.py ensure_superuser --email="$DJANGO_SUPERUSER_EMAIL" --password="$DJANGO_SUPERUSER_PASS"

exec "$@"
