**Projeto Auditoria**

Sistema de auditoria de logs, verificações e relatórios com Flask, Celery, RabbitMQ, Redis e PostgreSQL.

---

## 1. Pré-requisitos

- Docker & Docker Compose ou Python 3.11 + virtualenv
- Variáveis em `.env` (exemplo mínimo):
  ```dotenv
  DB_TYPE=docker
  DATABASE_URL=postgresql://postgres:yuri@db:5432/auditoria
  CELERY_BROKER_URL=redis://redis:6379/0
  CELERY_RESULT_BACKEND=redis://redis:6379/1
  RABBITMQ_DEFAULT_USER=guest
  RABBITMQ_DEFAULT_PASS=guest
  ```

---

## 2. Docker Compose

```bash
# Parar e remover volumes:
 docker-compose down -v

# Recriar imagens sem cache:
 docker-compose build --no-cache

# Iniciar serviços:
 docker-compose up
```

Após subir:

- UI RabbitMQ: [http://localhost:15672](http://localhost:15672) (`guest`/`guest`)
- UI Flower:   [http://localhost:5555](http://localhost:5555)

---

## 3. Banco de dados (local ou Docker)

```bash
python db/criar_tabelas.py     # criar
python db/deletar_tabelas.py   # deletar
python db/refrescar_tabelas.py # refresh
```

---

## 4. Flask

```bash
# Método 1: flask run
flask run --host=0.0.0.0 --port=5000

# Método 2: executar diretamente o app
python app.py
```

Acesse via navegador:

- Health check: `http://localhost:5000/health`
- Logs:         `http://localhost:5000/api/logs`
- Verificações: `http://localhost:5000/api/verificacoes`
- Relatórios:   `http://localhost:5000/api/relatorios`

---

## 5. Celery

- **Linux/macOS**:
  ```bash
  celery -A tasks.celery_app worker --loglevel=info
  ```
- **Windows** (pool solo):
  ```bash
  celery -A tasks.celery_app worker --loglevel=info --pool=solo
  ```

---



