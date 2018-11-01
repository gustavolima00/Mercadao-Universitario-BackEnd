default:
	pip install -r requirements.txt
	cd backend && python manage.py makemigrations
	cd backend && python manage.py migrate
	cd backend && python manage.py runserver 0.0.0.0:8000
update:
	pip install -r requirements.txt
	cd backend && python manage.py makemigrations
	cd backend && python manage.py migrate
run:
	cd backend && python manage.py runserver 0.0.0.0:8000

test:
	cd backend && python manage.py test