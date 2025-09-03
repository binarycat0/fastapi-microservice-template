install:
	uv sync

lint:
	uv run black ./src;
	uv run isort ./src;
	uv run mypy .;

test:
	uv run pytest

run:
	uv run uvicorn \
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

docker-migrate:
	docker compose \
	-f ./docker/docker-compose.yaml \
	--project-directory ./ \
	exec -w /app api uv run alembic -c /app/alembic.ini upgrade head

docker-downgrade:
	docker compose \
	-f ./docker/docker-compose.yaml \
	--project-directory ./ \
	exec -w /app api uv run alembic -c ./db/alembic.ini downgrade -1

docker-up: docker-compose-build docker-compose-up docker-migrate

docker-down:
	docker compose \
	-f ./docker/docker-compose.yaml \
	--project-directory ./ \
	down -v

migrate-check:
	uv run alembic -c ./alembic.ini check

migration:
ifndef m
	$(error m must be defined)
endif
	uv run alembic -c ./alembic.ini revision --autogenerate -m "$(m)"

migrate:
	uv run alembic -c ./alembic.ini upgrade head

downgrade:
	uv run alembic -c ./alembic.ini downgrade -1