install:
	poetry install

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

run:
	poetry run python manage.py runserver

create-user:
	poetry run python manage.py createsuperuser

test:
	poetry run python manage.py test