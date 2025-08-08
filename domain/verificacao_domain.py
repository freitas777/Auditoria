from datetime import datetime, timezone

class DominioVerificacao:
    def __init__(self, id_voto: int, comprovante: int):
        self.id_voto = id_voto
        self.comprovante = comprovante
        self.eh_valida = False
        self.mensagem_resultado = ""
        self.data_hora = datetime.now(timezone.utc)
        self.validar_dados()
        self.verificar_integridade()

    def validar_dados(self):
        if not isinstance(self.id_voto, int) or self.id_voto < 0:
            raise ValueError("O número de votos deve ser um inteiro não negativo.")
        if not isinstance(self.comprovante, int) or self.comprovante < 0:
            raise ValueError("O número de comprovante deve ser um inteiro não negativo.")

    def verificar_integridade(self):
        if self.id_voto == self.comprovante:
            self.eh_valida = True
            self.mensagem_resultado = "Integridade verificada com sucesso: O número de votos corresponde ao número de recibos."
        else:
            self.eh_valida = False
            self.mensagem_resultado = f"Falha na verificação de integridade: O número de votos ({self.id_voto}) não corresponde ao de recibos ({self.comprovante})."
    
    def executar_verificacao(self):
        return self.eh_valida, self.mensagem_resultado

    def para_dict(self):
        return {
            "eh_valida": self.eh_valida,
            "mensagem": self.mensagem_resultado,
            "id_voto": self.id_voto,
            "comprovante": self.comprovante,
            "data_hora": self.data_hora.isoformat()
        }