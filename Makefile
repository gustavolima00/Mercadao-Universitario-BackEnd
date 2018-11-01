default:
	pip install -r requirements.txt
	cd mercadao && python manage.py makemigrations
	cd mercadao && python manage.py migrate
	cd mercadao && python manage.py runserver 0.0.0.0:8000
update:
	pip install -r requirements.txt
	cd mercadao && python manage.py makemigrations
	cd mercadao && python manage.py migrate
run:
	cd mercadao && python manage.py runserver 0.0.0.0:8000

test:
	cd mercadao && python manage.py test