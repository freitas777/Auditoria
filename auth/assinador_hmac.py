import hmac
import hashlib
import os
import json
from datetime import datetime, timezone

class AssinadorHMAC:
    def __init__(self, chave_secreta: bytes = None):
        self.chave_secreta = chave_secreta if chave_secreta else os.getenv("LOG_HMAC_SECRET", "default_secret").encode('utf-8')

    def gerar_assinatura(self, dados: str) -> str:
        h = hmac.new(self.chave_secreta, dados.encode('utf-8'), hashlib.sha256)
        return h.hexdigest()

    def verificar_assinatura(self, dados: str, assinatura: str) -> bool:
        return hmac.compare_digest(self.gerar_assinatura(dados), assinatura)

    def _dados_para_assinatura(self, log_data) -> str:
        if isinstance(log_data, str):
            log_data = json.loads(log_data)
        campos_ordenados = sorted(log_data.items())
        return "&".join([f"{k}={v}" for k, v in campos_ordenados if v is not None])

    def assinar_log(self, log_data: dict) -> dict:
        dados_str = self._dados_para_assinatura(log_data)
        assinatura = self.gerar_assinatura(dados_str)
        log_data['assinatura'] = assinatura
        return log_data

    def validar_log(self, log_data: dict) -> bool:
        if 'assinatura' not in log_data:
            return False

        assinatura_original = log_data.pop('assinatura')
        dados_str = self._dados_para_assinatura(log_data)
        log_data['assinatura'] = assinatura_original
        
        return self.verificar_assinatura(dados_str, assinatura_original)