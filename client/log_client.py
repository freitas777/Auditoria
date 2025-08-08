import os
import sys
import grpc

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Importações geradas pelo protoc
from proto.log_pb2 import LogRequest, LogIdRequest
from proto.log_pb2_grpc import LogServiceStub
from google.protobuf.wrappers_pb2 import Int32Value, BoolValue

class ClienteLog:
    def __init__(self, target: str = "13.221.77.151:50051"):
        """Inicializa o cliente gRPC.
        
        Args:
            target (str): Endereço do servidor gRPC (padrão: "13.221.77.151:50051").
        """
        self.channel = grpc.insecure_channel(target) 
        self.stub = LogServiceStub(self.channel)

    def registrar_log(
        self,
        tipo: str,
        descricao: str,
        id_verificacao: int | None = None,
        voto_valido: bool = False,
        id_relatorio: int | None = None
    ):
        """Registra um novo log no servidor.
        
        Args:
            tipo (str): Tipo do log (ex: "ERRO", "INFO").
            descricao (str): Descrição detalhada.
            id_verificacao (int, optional): ID de verificação associado.
            voto_valido (bool, optional): Se o log está relacionado a um voto válido.
            id_relatorio (int, optional): ID de relatório associado.
        
        Returns:
            Resposta do servidor (depende da definição no .proto).
        """
        req = LogRequest(
            tipo=tipo,
            descricao=descricao,
            id_verificacao=Int32Value(value=id_verificacao) if id_verificacao is not None else None,
            voto_valido=BoolValue(value=voto_valido),
            id_relatorio=Int32Value(value=id_relatorio) if id_relatorio is not None else None
        )
        return self.stub.RegistrarLog(req)

    def buscar_log(self, id_log: int):
        """Busca um log pelo ID.
        
        Args:
            id_log (int): ID do log a ser buscado.
        
        Returns:
            Resposta do servidor (depende da definição no .proto).
        """
        req = LogIdRequest(id_log=id_log)
        return self.stub.BuscarLog(req)

    def __del__(self):
        """Fecha a conexão ao destruir o objeto."""
        if hasattr(self, 'channel'):
            self.channel.close()

if __name__ == "__main__":
    cliente = ClienteLog()
    try:
        resposta_registro = cliente.registrar_log(
            tipo="INFO",
            descricao="Teste de conexão do cliente gRPC",
            id_verificacao=123,
            voto_valido=True
        )
        print("Log registrado:", resposta_registro)
    except grpc.RpcError as e:
        print(f"Erro ao registrar log: {e.code()}: {e.details()}")
    try:
        resposta_busca = cliente.buscar_log(id_log=1)
        print("Log encontrado:", resposta_busca)
    except grpc.RpcError as e:
        print(f"Erro ao buscar log: {e.code()}: {e.details()}")