import grpc
from proto.relatorio_pb2 import RelatorioRequest
from proto.relatorio_pb2_grpc import RelatorioServiceStub
from google.protobuf.wrappers_pb2 import Int32Value

class ClienteRelatorio:
    def __init__(self, target="localhost:50051"):
        channel = grpc.insecure_channel(target)
        self.stub = RelatorioServiceStub(channel)

    def gerar_relatorio(self, tipo: str, formato: str, id_verificacao: int, criado_por: str):
        # Valida o formato antes de enviar a requisição
        formatos_validos = {"json", "txt", "pdf"}
        if formato.lower() not in formatos_validos:
            raise ValueError(f"Formato '{formato}' não suportado. Use: json, txt ou pdf")
            
        req = RelatorioRequest(
            tipo=tipo,
            formato=formato,
            id_verificacao=Int32Value(value=id_verificacao),
            criado_por=criado_por
        )
        return self.stub.GerarRelatorio(req)