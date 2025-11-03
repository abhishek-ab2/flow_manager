build:
	docker compose build

start:
	docker compose up -d

build-and-start:
    docker compose up --build -d

purge:
    docker compose down -v

shell:
	docker compose run --rm web /bin/sh
