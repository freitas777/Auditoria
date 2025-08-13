# Usa a versão BOOKWORM (Debian 12 estável)
FROM python:3.11-slim-bookworm

WORKDIR /app

# 1. Configura fontes APT para Bookworm e instala dependências
RUN echo "deb http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 2. Instalação otimizada do pip e pacotes
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip==23.3.1 && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

# 3. Fallback para psycopg2 (se necessário)
RUN pip install --no-cache-dir psycopg2-binary==2.9.7 || \
    (echo "Fallback: Building psycopg2 from source" && \
    pip install --no-cache-dir psycopg2==2.9.7)

COPY . .

EXPOSE 8080

CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "8080"]