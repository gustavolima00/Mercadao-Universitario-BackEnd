default:
	pip3 install -r requirements.txt
	cd backend && python3 manage.py makemigrations
	cd backend && python3 manage.py migrate
	cd backend && python3 manage.py runserver 0.0.0.0:8000
update:
	pip3 install -r requirements.txt
	cd backend && python3 manage.py makemigrations
	cd backend && python3 manage.py migrate
run:
	cd backend && python3 manage.py runserver 0.0.0.0:8000

test:
	cd backend && python3 manage.py test