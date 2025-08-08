import grpc
from sqlalchemy.orm import Session
from model.verificacao_model import Verificacao
from repository.verificacao_repository import RepositorioVerificacao
from proto import votacao_pb2_grpc, votacao_pb2

class ServicoVerificacao:
    def __init__(self, db: Session):
        self.db = db
        self.repositorio = RepositorioVerificacao(db)
        self.stub = votacao_pb2_grpc.VotacaoServiceStub(grpc.insecure_channel("13.221.77.151:50051"))

    def verificar_voto_por_id(self, id_voto: int, criado_por="sistema"):
        try:
            request = votacao_pb2.VotoValidoRequest(id_voto=id_voto)
            response = self.stub.GetVotoValido(request)

            resultado = response.valido
            mensagem = response.mensagem
            comprovante = {
                "id_voto": id_voto,
                "status": "válido" if resultado else "inválido",
                "mensagem": mensagem
            }

            return self.repositorio.salvar_verificacao(
                id_voto=id_voto,
                resultado=resultado,
                mensagem=mensagem,
                comprovante=comprovante,
                criado_por=criado_por
            )

        except grpc.RpcError as e:
            raise Exception(f"Erro ao se comunicar com serviço de votação: {e}")

    def buscar_verificacao(self, id_verificacao: int) -> Verificacao | None:
        return self.repositorio.buscar_verificacao_por_id(id_verificacao)
    
    def obter_votos_por_eleicao(self, id_eleicao: str) -> list:
        request = votacao_pb2.EleicaoVotosRequest(id_eleicao=id_eleicao)
        response = self.stub.GetEleicaoVotos(request)

        votos = []
        for voto in response.votos:
            votos.append({
                'id_voto': voto.id_voto,
                'id_candidato': voto.id_candidato,
                'data_voto': voto.data_voto
            })

        return votos
