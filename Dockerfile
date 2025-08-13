FROM python:3.11-slim

WORKDIR /app

# Instala dependências ESSENCIAIS (incluindo as do PostgreSQL)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instala o pip SEM atualizar (evita problemas com versões novas)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "8080"]