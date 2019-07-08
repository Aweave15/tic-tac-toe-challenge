start:
	docker-compose up

build:
	docker-compose build

test-flake8:
	flake8 .