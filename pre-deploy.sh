#!/bin/bash
python manage.py migrate

python seed.py
