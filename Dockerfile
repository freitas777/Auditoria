# Usa a imagem slim com compiladores básicos
FROM python:3.11-slim

WORKDIR /app

# 1. Instala dependências do sistema ANTES do pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# 2. Instalação segura de pacotes
RUN python -m pip install --no-cache-dir --upgrade pip==23.3.1 && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

# 3. Instalação específica do psycopg2 com fallback
RUN pip install --no-cache-dir psycopg2-binary==2.9.7 || \
    (echo "Fallback: instalando psycopg2 sem binary" && \
    pip install --no-cache-dir psycopg2==2.9.7)

COPY . .

EXPOSE 8080

CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "8080"]