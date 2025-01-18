FROM python:3.11-slim

RUN python -m pip install -U pip
RUN python -m pip install pipx
RUN pipx install poetry==1.8.4
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install
COPY ./src ./src

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000"]
