run:
	venv/bin/python manage.py runserver
migrate:
	python manage.py makemigrations
	python manage.py migrate
