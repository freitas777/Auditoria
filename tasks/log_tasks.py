from db.database import SessionLocal
from service.log_service import ServicoLog
from .celery_app import celery_app as app

@app.task(name="tasks.registrar_log_assincrono")
def registrar_log_assincrono(tipo: str, descricao: str, id_verificacao=None, id_relatorio=None):
    try:
        db = SessionLocal()
        service = ServicoLog(db)
        log = service.registrar_log(tipo, descricao, id_verificacao, id_relatorio)
        
        return log.para_dict()
    
    except Exception as e:
        app.logger.error(f"Erro ao registrar log: {str(e)}")
        return {
            "erro": str(e),
            "tipo": tipo,
            "descricao": descricao
        }
    
    finally:
        db.close()