#!/bin/sh

python manage.py migrated
python manage.py runserver 0.0.0.0:8000