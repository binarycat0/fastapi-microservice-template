
lint:
	poetry run black ./src;
	poetry run isort ./src;
	poetry run mypy .;

test:
	poetry run pytest

run:
	poetry run uvicorn \
	app:create_app \
	--app-dir src \
	--reload \
	--host 0.0.0.0 \
	--port 8000

docker-build:
	docker build -f ./docker/Dockerfile . -t ultimate-microservice

docker-compose-build:
	docker compose \
	-f ./docker/docker-compose.yaml \
	--project-directory ./ \
	build

docker-compose-up:
	docker compose \
	-f ./docker/docker-compose.yaml \
	--project-directory ./ \
	up -d

docker-up: docker-compose-build docker-compose-up

docker-down:
	docker compose \
	-f ./docker/docker-compose.yaml \
	--project-directory ./ \
	down -v

docker-migrate:
	docker compose \
	-f ./docker/docker-compose.yaml \
	--project-directory ./ \
	exec -w /app api poetry run alembic -c ./db/alembic.ini upgrade head

docker-downgrade:
	docker compose \
	-f ./docker/docker-compose.yaml \
	--project-directory ./ \
	exec -w /app api poetry run alembic -c ./db/alembic.ini downgrade -1

migrate-check:
	poetry run alembic -c ./alembic.ini check

migration:
ifndef m
	$(error m must be defined)
endif
	poetry run alembic -c ./alembic.ini revision --autogenerate -m "$(m)"

migrate:
	poetry run alembic -c ./alembic.ini upgrade head

downgrade:
	poetry run alembic -c ./alembic.ini downgrade -1