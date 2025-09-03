FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app
COPY uv.lock pyproject.toml ./
RUN uv sync --frozen
COPY ./src ./

EXPOSE 8000

ENTRYPOINT ["uv", "run", "uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000"]
