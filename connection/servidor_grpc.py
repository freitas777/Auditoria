import os
import sys
import grpc
from concurrent import futures
import signal
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connection.servico_grpc_manipuladores import ManipuladorLog, ManipuladorVerificacao, ManipuladorRelatorio
from proto import log_pb2_grpc, verificacao_pb2_grpc, relatorio_pb2_grpc

def iniciar_servidor_grpc():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    log_pb2_grpc.add_LogServiceServicer_to_server(ManipuladorLog(), servidor)
    verificacao_pb2_grpc.add_VerificacaoServiceServicer_to_server(ManipuladorVerificacao(), servidor)
    relatorio_pb2_grpc.add_RelatorioServiceServicer_to_server(ManipuladorRelatorio(), servidor)
    
    porta = os.getenv("PORTA_GRPC", "50051")
    endereco = f'[::]:{porta}'
    servidor.add_insecure_port(endereco)
    
    def encerrar_servidor(signum, frame):
        print(f"\n{datetime.now(timezone.utc)} - Encerrando servidor gRPC...")
        servidor.stop(0)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, encerrar_servidor)
    signal.signal(signal.SIGTERM, encerrar_servidor)
    
    print(f"\n🟢 {datetime.now(timezone.utc)} - Servidor gRPC iniciado com sucesso em {endereco}")
    print("🟢 Pronto para receber requisições...")
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor_grpc()