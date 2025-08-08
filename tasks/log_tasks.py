from db.database import SessionLocal
from service.log_service import ServicoLog
from .celery_app import celery_app as app

@app.task(name="tasks.registrar_log_assincrono")
def registrar_log_assincrono(tipo: str, descricao: str, id_verificacao: int, voto_valido: int, id_relatorio: int):
    # try:
    #     id_verificacao = int(id_verificacao) if id_verificacao else None
    # except (TypeError, ValueError):
    #     id_verificacao = None
        
    # try:
    #     id_relatorio = int(id_relatorio) if id_relatorio else None
    # except (TypeError, ValueError):
    #     id_relatorio = None
        
    # try:
    #     voto_valido = bool(voto_valido) if voto_valido is not None else False
    # except (TypeError, ValueError):
    #     voto_valido = False

    try:
        db = SessionLocal()
        service = ServicoLog(db)
        log = service.registrar_log(tipo, descricao, id_verificacao, voto_valido, id_relatorio)
        return log.para_dict()
    except Exception as e:
        raise
    finally:
        db.close()