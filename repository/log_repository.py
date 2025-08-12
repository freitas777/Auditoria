from sqlalchemy.orm import Session
from model.log_model import Log
import math

class RepositorioLog:
    def __init__(self, db: Session):
        self.db = db

    def salvar_log(
        self,
        tipo: str,
        descricao: str,
        id_verificacao: int | None,
        id_relatorio: int | None,
        assinatura: str
    ) -> Log:
        log = Log(
            tipo=tipo,
            descricao=descricao,
            id_verificacao=id_verificacao,
            id_relatorio=id_relatorio,
            assinatura=assinatura
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def buscar_log_por_id(self, id_log: int) -> Log | None:
        return self.db.query(Log).filter(Log.id_log == id_log).first()

    def listar_logs_paginados(self, pagina: int = 1, limite: int = 10) -> tuple[list[Log], int]:
        offset = (pagina - 1) * limite
        logs = self.db.query(Log).offset(offset).limit(limite).all()
        total_logs = self.db.query(Log).count()
        total_paginas = math.ceil(total_logs / limite)
        return logs, total_paginas