#!/usr/bin/env bash
# exit on error
set -o errexit  

pip install -r requirements.txt

# collect static files
python manage.py collectstatic --noinput

# apply database migrations
python manage.py migrate
