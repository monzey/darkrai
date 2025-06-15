FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml poetry.lock* README.md ./
COPY src ./src

RUN poetry config virtualenvs.create false && \
    poetry install --no-ansi
