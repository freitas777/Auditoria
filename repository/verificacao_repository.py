import json
from sqlalchemy.orm import Session
from model.verificacao_model import Verificacao

class RepositorioVerificacao:
    def __init__(self, db: Session):
        self.db = db

    def salvar_verificacao(self, id_voto, resultado, mensagem, comprovante, criado_por):
        nova = Verificacao(
            id_voto=id_voto,
            comprovante=json.dumps(comprovante),
            resultado=resultado,
            mensagem=mensagem,
            criado_por=criado_por
        )
        self.db.add(nova)
        self.db.commit()
        self.db.refresh(nova)
        return nova

    def buscar_verificacao_por_id(self, id_verificacao: int):
        return self.db.query(Verificacao).filter(Verificacao.id_verificacao == id_verificacao).first()

    def listar_verificacoes(self):
        return self.db.query(Verificacao).all()

    def listar_verificacoes_paginadas(self, pagina: int, limite: int):
        total = self.db.query(Verificacao).count()
        verificacoes = self.db.query(Verificacao).offset((pagina - 1) * limite).limit(limite).all()
        total_paginas = (total + limite - 1) // limite
        return verificacoes, total_paginas
