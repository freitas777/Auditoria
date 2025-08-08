import grpc
from db.database import SessionLocal
from service.log_service import ServicoLog
from service.verificacao_service import ServicoVerificacao
from service.relatorio_service import ServicoRelatorio
from proto import log_pb2, verificacao_pb2, relatorio_pb2
from proto import log_pb2_grpc, verificacao_pb2_grpc, relatorio_pb2_grpc
from google.protobuf.wrappers_pb2 import Int32Value, BoolValue
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timezone

class ManipuladorLog(log_pb2_grpc.LogServiceServicer):
    def __init__(self):
        self.db = SessionLocal()
        self.servico = ServicoLog(self.db)

    def RegistrarLog(self, requisicao, contexto):
        try:
            log = self.servico.registrar_log(
                tipo=requisicao.tipo,
                descricao=requisicao.descricao,
                id_verificacao=requisicao.id_verificacao.value if requisicao.HasField("id_verificacao") else None,
                voto_valido=requisicao.voto_valido.value if requisicao.HasField("voto_valido") else False,
                id_relatorio=requisicao.id_relatorio.value if requisicao.HasField("id_relatorio") else None
            )

            carimbo_tempo = Timestamp()
            carimbo_tempo.FromDatetime(log.data_hora.astimezone(timezone.utc))

            return log_pb2.LogResponse(
                status="sucesso",
                mensagem="Log registrado com sucesso",
                id_log=log.id_log,
                tipo=log.tipo,
                descricao=log.descricao,
                data_hora=carimbo_tempo,
                id_verificacao=Int32Value(value=log.id_verificacao) if log.id_verificacao else None,
                voto_valido=BoolValue(value=log.voto_valido),
                id_relatorio=Int32Value(value=log.id_relatorio) if log.id_relatorio else None,
                assinatura=log.assinatura,
                valido=True
            )
        except Exception as erro:
            contexto.set_details(str(erro))
            contexto.set_code(grpc.StatusCode.INTERNAL)
            return log_pb2.LogResponse()
    
    def __del__(self):
        self.db.close()

class ManipuladorVerificacao(verificacao_pb2_grpc.VerificacaoServiceServicer):
    def __init__(self):
        self.db = SessionLocal()
        self.servico = ServicoVerificacao(self.db)

    def ExecutarVerificacao(self, requisicao, contexto):
        try:
            verificacao = self.servico.verificar_integridade(
                votos=requisicao.votos,
                recibos=requisicao.recibos,
                criado_por=requisicao.criado_por
            )

            carimbo_tempo = Timestamp()
            carimbo_tempo.FromDatetime(verificacao.data_hora.astimezone(timezone.utc))

            return verificacao_pb2.VerificacaoResponse(
                status="sucesso",
                mensagem="Verificação realizada",
                id_verificacao=verificacao.id_verificacao,
                votos=verificacao.votos,
                recibos=verificacao.recibos,
                resultado=verificacao.resultado,
                mensagem=verificacao.mensagem,
                criado_por=verificacao.criado_por,
                data_hora=carimbo_tempo
            )
        except Exception as erro:
            contexto.set_details(str(erro))
            contexto.set_code(grpc.StatusCode.INTERNAL)
            return verificacao_pb2.VerificacaoResponse()
    
    def __del__(self):
        self.db.close()

class ManipuladorRelatorio(relatorio_pb2_grpc.RelatorioServiceServicer):
    def __init__(self):
        self.db = SessionLocal()
        self.servico = ServicoRelatorio(self.db)

    def GerarRelatorio(self, requisicao, contexto):
        try:
            formatos_validos = {"json", "txt", "pdf"}
            if requisicao.formato.lower() not in formatos_validos:
                raise ValueError(f"Formato '{requisicao.formato}' não suportado")
                
            relatorio = self.servico.gerar_relatorio(
                tipo=requisicao.tipo,
                formato=requisicao.formato,
                id_verificacao=requisicao.id_verificacao.value,
                criado_por=requisicao.criado_por
            )

            carimbo_tempo = Timestamp()
            carimbo_tempo.FromDatetime(relatorio.data_hora.astimezone(timezone.utc))

            return relatorio_pb2.RelatorioResponse(
                status="sucesso",
                mensagem="Relatório gerado",
                id_relatorio=relatorio.id_relatorio,
                tipo=relatorio.tipo,
                formato=relatorio.formato,
                caminho=relatorio.caminho,
                criado_por=relatorio.criado_por,
                id_verificacao=relatorio.id_verificacao,
                data_hora=carimbo_tempo
            )
        except Exception as erro:
            contexto.set_details(str(erro))
            contexto.set_code(grpc.StatusCode.INTERNAL)
            return relatorio_pb2.RelatorioResponse()
    
    def __del__(self):
        self.db.close()