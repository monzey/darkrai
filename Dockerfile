FROM python:3.11-slim

WORKDIR /app

RUN apt update && apt install -y build-essential cmake git
RUN pip install --upgrade pip && \
    pip install poetry

RUN poetry config virtualenvs.create false
