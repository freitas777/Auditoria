FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_TYPE=docker

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libpq-dev postgresql-client netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
RUN chmod +x start.sh

ENV PYTHONPATH=/app
EXPOSE 5000 50051

ENTRYPOINT ["./start.sh"]