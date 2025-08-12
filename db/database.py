from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

def is_docker():
    return os.environ.get('DOCKER_ENV') == "true"

if is_docker():
    DATABASE_URL = os.getenv("DOCKER_DATABASE_URL")
else:
    DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from model.log_model import Log  
from model.verificacao_model import Verificacao  
from model.relatorio_model import Relatorio  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def close_session():
    if SessionLocal:
        SessionLocal.close_all()