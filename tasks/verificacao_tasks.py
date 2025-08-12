from db.database import SessionLocal
from service.verificacao_service import ServicoVerificacao
from .celery_app import celery_app as app

@app.task(name="tasks.executar_verificacao_assincrono")
def executar_verificacao_assincrono(votos: int, recibos: int, criado_por: str):
    db = SessionLocal()
    try:
        servico = ServicoVerificacao(db)
        verificacao = servico.verificar_integridade(votos, recibos, criado_por)
        return {
            "status": "sucesso",
            "id_verificacao": verificacao.id_verificacao,
            "resultado": verificacao.resultado
        }
    except Exception as e:
        raise
    finally:
        db.close()