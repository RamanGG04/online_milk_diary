#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input

if [ "$CREATE_SUPERUSER" = "true" ]; then
  python manage.py setup_demo_data
fi
