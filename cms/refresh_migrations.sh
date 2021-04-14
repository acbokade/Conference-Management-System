rm -rf accounts/migrations conference/migrations gsp/migrations reviewer/migrations
python manage.py makemigrations accounts
python manage.py makemigrations conference
python manage.py makemigrations gsp
python manage.py makemigrations reviewer
python manage.py migrate