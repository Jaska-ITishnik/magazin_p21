mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

super:
	python3 manage.py createsuperuser
run:
	python3 manage.py runserver

celery:
	celery -A root worker -l INFO