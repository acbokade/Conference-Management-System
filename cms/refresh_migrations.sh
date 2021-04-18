#!/bin/bash
rm -rf accounts/migrations conference/migrations gsp/migrations reviewer/migrations area_chair/migrations
rm db.sqlite3
python3 manage.py makemigrations accounts
python3 manage.py makemigrations conference
python3 manage.py makemigrations gsp
python3 manage.py makemigrations reviewer
python3 manage.py makemigrations area_chair
python3 manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('cms', 'admin@example.com', 'cms')" | python3 manage.py shell