from db.database import SessionLocal
from service.relatorio_service import ServicoRelatorio
from .celery_app import celery_app as app

@app.task(name="tasks.gerar_relatorio_assincrono")
def gerar_relatorio_assincrono(tipo: str, formato: str, id_verificacao: int, criado_por: str):
    db = SessionLocal()
    try:
        servico = ServicoRelatorio(db)
        relatorio = servico.gerar_relatorio(tipo, formato, id_verificacao, criado_por)
        return {
            "status": "sucesso",
            "id_relatorio": relatorio.id_relatorio,
            "caminho": relatorio.caminho
        }
    except Exception as e:
        # Registrar o erro para debug
        app.logger.error(f"Erro ao gerar relatório assíncrono: {str(e)}")
        raise
    finally:
        db.close()