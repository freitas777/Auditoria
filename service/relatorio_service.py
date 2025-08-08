import os
from repository.relatorio_repository import RepositorioRelatorio
from domain.relatorio_domain import DominioRelatorio
from tasks.log_tasks import registrar_log_assincrono
from model.log_model import Log

class ServicoRelatorio:
    FORMATOS_SUPORTADOS = {"txt", "json", "pdf"}
    
    def __init__(self, db=None):
        self.db = db
        self.repo = RepositorioRelatorio(db)
        self.dominio = DominioRelatorio()

    def gerar_relatorio(self, tipo: str, formato: str, id_verificacao: int, criado_por: str):
        logs = self.db.query(Log).filter(Log.id_verificacao == id_verificacao).all()
        logs_dict = [log.para_dict() for log in logs]
        
        caminho_arquivo = self.dominio.criar_arquivo_relatorio(
            logs=logs_dict,
            formato=formato,
            tipo=tipo,
            id_verificacao=id_verificacao
        )
        
        relatorio = self.repo.salvar_relatorio(
            tipo=tipo,
            formato=formato,
            caminho=caminho_arquivo,
            criado_por=criado_por,
            id_verificacao=id_verificacao
        )
        
        registrar_log_assincrono.delay(
            "RELATORIO_GERADO",
            f"Relatório {tipo} gerado em {formato}",
            id_relatorio=relatorio.id_relatorio
        )
        return relatorio


    def buscar_relatorio(self, id_relatorio: int):
        return self.repo.buscar_relatorio(id_relatorio)

    def remover_relatorio(self, id_relatorio: int):
        relatorio = self.repo.buscar_relatorio(id_relatorio)
        if not relatorio:
            raise ValueError(f"Relatório {id_relatorio} não encontrado")
        
        try:
            if os.path.exists(relatorio.caminho):
                os.remove(relatorio.caminho)
            self.repo.remover_relatorio(id_relatorio)
        except OSError as e:
            registrar_log_assincrono.delay(
                tipo="ERRO",
                descricao=f"Erro ao remover arquivo do relatório {id_relatorio}: {e}",
                id_relatorio=id_relatorio
            )
            raise