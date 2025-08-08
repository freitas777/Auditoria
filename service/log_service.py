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

        canal = grpc.insecure_channel('13.221.77.151:50051')
        self.stub = votacao_pb2_grpc.VotacaoServiceStub(canal)

    def registrar_log(
        self,
        tipo: str,
        descricao: str,
        id_verificacao: int | None = None,
        voto_valido: bool = False,
        id_relatorio: int | None = None,
        id_voto: str | None = None
    ) -> Log:
        
        if id_voto:
            try:
                request = votacao_pb2.VotoValidoRequest(id_voto=id_voto)
                response = self.stub.GetVotoValido(request)
                voto_valido = response.valido
                descricao += f" | Verificação de voto: {response.mensagem}"
            except grpc.RpcError as e:
                descricao += f" | ERRO gRPC: {e.details()}"
        
        log_data = {
            "tipo": tipo,
            "descricao": descricao,
            "id_verificacao": id_verificacao,
            "voto_valido": voto_valido,
            "id_relatorio": id_relatorio,
            "data_hora": datetime.now(timezone.utc)
        }
        
        log_data_formatado = validar_e_formatar_log(log_data["tipo"], log_data["descricao"])
        log_assinado = self.assinador.assinar_log(log_data_formatado)

        log = self.repositorio.salvar_log(
            tipo=log_assinado['tipo'],
            descricao=log_assinado['descricao'],
            id_verificacao=log_assinado['id_verificacao'],
            voto_valido=log_assinado['voto_valido'],
            id_relatorio=log_assinado['id_relatorio'],
            assinatura=log_assinado['assinatura']
        )
        return log

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
