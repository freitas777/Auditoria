from google.protobuf.timestamp_pb2 import Timestamp
def validar_e_formatar_log(tipo: str, mensagem: str) -> str:
    tipos_validos = {"INFO", "AVISO", "ERRO", "DEBUG"}
    tipo_upper = tipo.strip().upper()
    if tipo_upper not in tipos_validos:
        raise ValueError(f"Tipo de log inválido: {tipo}")
    return f"[{tipo_upper}] {mensagem.strip()}"
