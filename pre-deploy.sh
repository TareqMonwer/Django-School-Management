#!/bin/bash
set -e

python manage.py migrate --noinput

python seed.py
