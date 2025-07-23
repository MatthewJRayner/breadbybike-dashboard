#!/usr/bin/env bash
cd ..
set -o errexit
pip install -r requirements.txt
cd backend
python manage.py collectstatic --no-input
python manage.py migrate 