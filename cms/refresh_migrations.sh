#!/bin/bash
rm -rf accounts/migrations conference/migrations gsp/migrations reviewer/migrations area_chair/migrations
python3 manage.py makemigrations accounts
python3 manage.py makemigrations conference
python3 manage.py makemigrations gsp
python3 manage.py makemigrations reviewer
python3 manage.py makemigrations area_chair
python3 manage.py migrate
