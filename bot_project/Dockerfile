FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY ../requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade "async-timeout>=4.0,<5.0" && \
    pip install --no-cache-dir -r requirements.txt

COPY . .