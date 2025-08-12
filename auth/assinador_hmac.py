import hmac
import hashlib
import os

class AssinadorHMAC:
    def __init__(self, chave_secreta: str = None):
        # Use uma chave padrão se não for fornecida
        self.chave_secreta = chave_secreta or os.getenv("CHAVE_ASSINATURA", "chave-padrao-segura")
        
        # Garanta que a chave seja bytes
        if isinstance(self.chave_secreta, str):
            self.chave_secreta = self.chave_secreta.encode('utf-8')

    def assinar_log(self, log_formatado: str) -> str:
        """Gera assinatura HMAC-SHA256 para o log formatado"""
        try:
            # Converta para bytes se necessário
            if isinstance(log_formatado, str):
                log_bytes = log_formatado.encode('utf-8')
            else:
                log_bytes = log_formatado
                
            return hmac.new(
                self.chave_secreta,
                log_bytes,
                hashlib.sha256
            ).hexdigest()
            
        except Exception as e:
            print(f"Erro na assinatura: {str(e)}")
            return "ERRO_ASSINATURA"

    def validar_log(self, log_formatado: str, assinatura: str) -> bool:
        """Valida a assinatura do log"""
        try:
            assinatura_calculada = self.assinar_log(log_formatado)
            return hmac.compare_digest(assinatura_calculada, assinatura)
        except:
            return False