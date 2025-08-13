FROM python:3.11-slim 

WORKDIR /app

# Instala dependências do sistema e Python em uma única camada
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt psycopg2-binary

COPY . .

EXPOSE 8080

CMD ["python", "app.py", “--host”, “0.0.0.0”, “-port”, 8080]