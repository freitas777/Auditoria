import grpc
from proto.verificacao_pb2 import VerificacaoRequest
from proto.verificacao_pb2_grpc import VerificacaoServiceStub
from datetime import datetime, timezone

class ClienteVerificacao:
    def __init__(self, target="localhost:50051"):
        channel = grpc.insecure_channel(target)
        self.stub = VerificacaoServiceStub(channel)

    def verificar_integridade(self, votos: int, recibos: int, criado_por: str = "grpc_user"):
        req = VerificacaoRequest(votos=votos, recibos=recibos, criado_por=criado_por)
        return self.stub.ExecutarVerificacao(req)