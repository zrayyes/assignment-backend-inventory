backend = store-backend
exec = docker-compose exec

default:
	echo "Ready"

up:
	docker-compose up --build -d

up-no-build:
	docker-compose up -d

stop:
	docker-compose stop

remove:
	docker-compose rm -f

logs:
	docker-compose logs -f

shell:
	$(exec) $(backend) sh

test:
	$(exec) -e SANIC_ENV=testing $(backend) pytest src/tests

flake:
	$(exec) $(backend) flake8 src

black:
	$(exec) $(backend) black src

isort:
	$(exec) $(backend) isort src

format: black flake isort

create_db:
	$(exec) $(backend) python manage.py create_db

seed_db:
	$(exec) $(backend) python manage.py create_db seed_db
