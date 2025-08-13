FROM python:3.11-slim 

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    RUN pip install psycopg2-binary

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "python app.py"]