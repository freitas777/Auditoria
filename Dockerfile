FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema necessárias para o psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Instala psycopg2 com compilação otimizada
RUN pip install --no-cache-dir psycopg2-binary==2.9.7

COPY . .

EXPOSE 8080

# Corrigindo o comando CMD (aspas retas e sintaxe correta)
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "8080"]