.PHONY: build up seed shell

build:
	docker compose build

up:
	docker compose up --build

shell:
	docker compose run --rm web /bin/sh
