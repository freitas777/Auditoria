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
                "status": resultado,
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

    def gerar_relatorio_votos(self, id_eleicao: str):
        try:
            try:
                id_eleicao_int = int(id_eleicao)
            except ValueError:
                id_eleicao_int = 0  
            if not id_eleicao or not isinstance(id_eleicao, str):
                raise ValueError("ID de eleição inválido")
            
            relatorio = {
                "id_eleicao": id_eleicao,
                "total_votos": 0,
                "votos_validos": 0,
                "votos_invalidos": 0,
                "percentual_valido": 0.0,
                "detalhes_votos": [],
                "erros": []
            }
            
            try:
                request = votacao_pb2.EleicaoVotosRequest(id_eleicao=id_eleicao_int)
                response = self.stub.GetEleicaoVotos(request)
                votos = response.votos
            except grpc.RpcError as e:
                relatorio["erros"].append(f"Erro gRPC: {e.code().name} - {e.details()}")
                votos = []
            except Exception as e:
                relatorio["erros"].append(f"Erro inesperado: {str(e)}")
                votos = []
            
            for i, voto_info in enumerate(votos):
                try:
                    id_voto = str(voto_info.id_voto) if hasattr(voto_info, 'id_voto') else f"ERRO-{i}"
                    
                    try:
                        voto_request = votacao_pb2.VotoValidoRequest(id_voto=id_voto)
                        voto_response = self.stub.GetVotoValido(voto_request)
                        valido = bool(voto_response.valido)
                        mensagem = str(voto_response.mensagem)
                    except:
                        valido = False
                        mensagem = "Erro na verificação"
                    
                    try:
                        id_candidato = int(voto_info.id_candidato)
                    except:
                        id_candidato = -1
                    
                    relatorio["total_votos"] += 1
                    if valido:
                        relatorio["votos_validos"] += 1
                    
                    relatorio["detalhes_votos"].append({
                        'id_voto': id_voto,
                        'id_candidato': id_candidato,
                        'valido': valido,
                        'mensagem': mensagem
                    })
                    
                except Exception as e:
                    relatorio["erros"].append(f"Erro processando voto {i}: {str(e)}")
                    relatorio["detalhes_votos"].append({
                        'id_voto': f"ERRO-{i}",
                        'id_candidato': -1,
                        'valido': False,
                        'mensagem': f"Erro: {str(e)}"
                    })
            
            if relatorio["total_votos"] > 0:
                relatorio["votos_invalidos"] = relatorio["total_votos"] - relatorio["votos_validos"]
                relatorio["percentual_valido"] = round(
                    (relatorio["votos_validos"] / relatorio["total_votos"]) * 100, 
                    2
                )
            
            return relatorio
            
        except Exception as e:
            import traceback
            return {
                "id_eleicao": id_eleicao,
                "erro_critico": f"Falha catastrófica: {str(e)}",
                "traceback": traceback.format_exc()
            }
    
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
