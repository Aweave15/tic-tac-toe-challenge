start:
	docker-compose up

build:
	docker-compose build

test:
	docker-compose run --rm web py.test tests/
	
test-flake8:
	flake8 .