from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:lucas123@db:5432/auditoria_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
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