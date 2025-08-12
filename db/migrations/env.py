import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
print(f"[Alembic] Diretório raiz do projeto adicionado ao PATH: {project_root}")

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração do Alembic ---
config = context.config

# Configura o sistema de logging do Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    print("[Alembic] Configuração de logging carregada.")
else:
    print("[Alembic] Nenhum arquivo de configuração de logging encontrado.")

# --- Determinação da URL do Banco de Dados ---
def is_docker_env():
    """Verifica se o ambiente atual é Docker."""
    return os.environ.get('DOCKER_ENV', 'false').lower() == "true"

if is_docker_env():
    database_url = "postgresql://lucas:123@db:5433/auditoria_db"
    env_type = "Docker/EC2"
else:
    database_url = os.getenv("LOCAL_DATABASE_URL")
    env_type = "local"

if not database_url:
    print(f"[Alembic] ERRO: Variável de ambiente para {env_type} DATABASE_URL não definida!")
    # Você pode optar por levantar uma exceção aqui ou sair
    raise ValueError(f"URL do banco de dados não configurada para o ambiente {env_type}.")

print(f"[Alembic] Ambiente {env_type} detectado. Usando URL: {database_url}")
config.set_main_option('sqlalchemy.url', database_url)

# --- Importação da Base e dos Modelos ---
target_metadata = None
try:
    from db.database import Base
    # Importe explicitamente todos os modelos para que o Alembic os detecte
    from model.log_model import Log
    from model.verificacao_model import Verificacao
    from model.relatorio_model import Relatorio
    
    target_metadata = Base.metadata
    if target_metadata and target_metadata.tables:
        print(f"[Alembic] Metadados importados com sucesso. Tabelas detectadas: {list(target_metadata.tables.keys())}")
    else:
        print("[Alembic] Metadados importados, mas nenhuma tabela detectada. Verifique se os modelos estão definidos corretamente.")
except ImportError as e:
    print(f"[Alembic] ERRO ao importar modelos: {e}. Certifique-se de que o caminho para 'db.database' e 'model.*' está correto e os arquivos existem.")
except Exception as e:
    print(f"[Alembic] Ocorreu um erro inesperado ao importar metadados: {e}")

# --- Funções de Migração ---
def run_migrations_offline():
    """Executa migrações no modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True, # Permite a comparação de tipos para detecção de mudanças
        render_as_batch=True # Útil para alguns bancos de dados, como SQLite, ao alterar tabelas
    )

    print("[Alembic] Executando migrações no modo OFFLINE...")
    with context.begin_transaction():
        context.run_migrations()
    print("[Alembic] Migrações offline concluídas.")

def run_migrations_online():
    """Executa migrações no modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool, # Usar NullPool para evitar problemas de conexão em migrações
    )

    print("[Alembic] Executando migrações no modo ONLINE...")
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True
        )

        try:
            with context.begin_transaction():
                context.run_migrations()
            print("[Alembic] Migrações online aplicadas com sucesso.")
        except Exception as e:
            print(f"[Alembic] ERRO ao aplicar migrações online: {e}")
            raise # Re-lança a exceção para que o Alembic falhe

# --- Execução Principal ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()