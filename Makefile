run:
	venv/bin/python manage.py runserver
migrate:
	venv/bin/python manage.py makemigrations
	venv/bin/python manage.py migrate 
