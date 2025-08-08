import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

def is_docker():
    return os.environ.get('DOCKER_ENV') == "true"

if is_docker():
    BROKER_URL = os.getenv("DOCKER_CELERY_BROKER_URL")
else:
    BROKER_URL = os.getenv("LOCAL_CELERY_BROKER_URL")

if not BROKER_URL:
    raise ValueError("CELERY_BROKER_URL não configurada no ambiente.")

celery_app = Celery(
    "tasks",
    broker=BROKER_URL,
    backend="rpc://",
    include=[
        "tasks.log_tasks",
        "tasks.relatorio_tasks",
        "tasks.verificacao_tasks"
    ]
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

print(f"[Celery] Aplicação Celery configurada com broker: {BROKER_URL}")

if __name__ == '__main__':
    celery_app.start()