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

pytest:
	$(exec) $(backend) pytest src/tests

lint:
	$(exec) $(backend) flake8 src

format:
	$(exec) $(backend) black src

isort:
	$(exec) $(backend) isort src
