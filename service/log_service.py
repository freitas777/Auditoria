import grpc
from sqlalchemy.orm import Session
from repository.log_repository import RepositorioLog
from domain.log_domain import validar_e_formatar_log
from proto import votacao_pb2, votacao_pb2_grpc
from model.log_model import Log
from datetime import datetime, timezone
from auth.assinador_hmac import AssinadorHMAC

class ServicoLog:
    def __init__(self, db: Session):
        self.db = db
        self.repositorio = RepositorioLog(db)
        self.assinador = AssinadorHMAC()

        self.assinador = AssinadorHMAC("123")

    def registrar_log(
        self,
        tipo: str,
        descricao: str,
        id_verificacao: int | None = None,
        id_relatorio: int | None = None,
        id_voto: str | None = None
    ) -> Log:
        # 1. Processar verificação de voto se necessário
        if id_voto and self.stub:
            try:
                request = votacao_pb2.VotoValidoRequest(id_voto=id_voto)
                response = self.stub.GetVotoValido(request)
                descricao += f" | Verificação de voto: {response.mensagem}"
            except grpc.RpcError as e:
                descricao += f" | ERRO gRPC: {e.details()}"
            except Exception as e:
                descricao += f" | ERRO: {str(e)}"

        # 2. Validar e formatar o log
        try:
            log_formatado = validar_e_formatar_log(tipo, descricao)
        except ValueError as e:
            # Usar valores padrão se validação falhar
            log_formatado = f"[ERRO] {str(e)}"

        assinatura = self.assinador.assinar_log(log_formatado)

        # 4. Salvar no banco de dados
        try:
            log = self.repositorio.salvar_log(
                tipo=tipo,  # Tipo original
                descricao=descricao,  # Descrição original
                id_verificacao=id_verificacao,
                id_relatorio=id_relatorio,
                assinatura=assinatura
            )
            return log
        except Exception as e:
            print(f"Erro ao salvar log: {str(e)}")
            raise

    def buscar_log(self, id_log: int) -> Log | None:
        log = self.repositorio.buscar_log_por_id(id_log)
        if not log:
            return None
            
        log_dict = log.para_dict()
        log.valido = self.assinador.validar_log(log_dict)
        return log

    def listar_logs_paginados(self, pagina: int, limite: int) -> tuple[list[Log], int]:
        logs, total_paginas = self.repositorio.listar_logs_paginados(pagina, limite)
        for log in logs:
            log_dict = log.para_dict()
            log.valido = self.assinador.validar_log(log_dict)
        return logs, total_paginas
