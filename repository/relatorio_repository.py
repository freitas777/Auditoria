from sqlalchemy.orm import Session
from model.relatorio_model import Relatorio
import math

class RepositorioRelatorio:
    def __init__(self, db: Session):
        self.db = db

    def salvar_relatorio(
        self, tipo: str, formato: str, caminho: str, criado_por: str, id_verificacao: int
    ) -> Relatorio:
        relatorio = Relatorio(
            tipo=tipo,
            formato=formato,
            caminho=caminho,
            criado_por=criado_por,
            id_verificacao=id_verificacao
        )
        self.db.add(relatorio)
        self.db.commit()
        self.db.refresh(relatorio)
        return relatorio

    def buscar_relatorio(self, id_relatorio: int) -> Relatorio | None:
        return self.db.query(Relatorio).filter(Relatorio.id_relatorio == id_relatorio).first()

    def listar_relatorios_paginados(self, pagina: int = 1, por_pagina: int = 50) -> tuple[list[Relatorio], int]:
        total = self.db.query(Relatorio).count()
        itens = (
            self.db.query(Relatorio)
              .order_by(Relatorio.data_hora.desc())
              .offset((pagina - 1) * por_pagina)
              .limit(por_pagina)
              .all()
        )
        paginas = math.ceil(total / por_pagina)
        return itens, paginas

    def remover_relatorio(self, id_relatorio: int) -> None:
        relatorio = self.buscar_relatorio(id_relatorio)
        if relatorio:
            self.db.delete(relatorio)
            self.db.commit()