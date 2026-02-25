#!/bin/bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python seed.py
