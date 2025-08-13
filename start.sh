#!/bin/bash

wait_for_service() {
    host="$1"
    port="$2"
    service_name="$3"
    
    echo ">>> Aguardando $service_name ($host:$port) ..."
    while ! nc -z "$host" "$port"; do
        sleep 1
    done
    echo ">>> $service_name pronto!"
}

wait_for_service db 5433 "Banco de Dados"
wait_for_service rabbitmq 5672 "RabbitMQ"

if [ "$TIPO_SERVICO" = "app" ]; then
    echo ">>> Compilando Protobufs..."
    python -m grpc_tools.protoc -I./proto --python_out=./proto --grpc_python_out=./proto ./proto/*.proto

    echo ">>> Ajustando imports gerados..."
    for file in ./proto/*_pb2_grpc.py; do
        sed -i 's/^import \(.*\)_pb2 as/from proto import \1_pb2 as/' "$file"
    done

    echo ">>> Aplicando migrações Alembic..."
    alembic -c db/alembic.ini upgrade head
fi

if [ "$TIPO_SERVICO" = "app" ]; then
    echo ">>> Iniciando servidor Flask e gRPC..."
    python app.py &
    python connection/servidor_grpc.py
elif [ "$TIPO_SERVICO" = "worker" ]; then
    echo ">>> Iniciando serviço 'worker'..."
    celery -A tasks.celery_app worker --loglevel=info --pool=solo --concurrency=1
fi