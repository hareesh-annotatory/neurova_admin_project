#!/usr/bin/env bash
set -e
source .venv/bin/activate
python manage.py check
python scripts/create_superuser.py
python manage.py runserver 0.0.0.0:8001
