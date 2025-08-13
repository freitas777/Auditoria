FROM python:3.11-slim 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install psycopg2-binary

COPY . .

EXPOSE 8080

CMD ["python", "app.py", “--host”, “0.0.0.0”, “-port”, 8080]