from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime, timezone

class Log(Base):
    __tablename__ = "logs"
    
    id_log = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    id_verificacao = Column(Integer, ForeignKey('verificacoes.id_verificacao', ondelete="SET NULL"), nullable=True)
    id_relatorio = Column(Integer, ForeignKey('relatorios.id_relatorio', ondelete="SET NULL"), nullable=True)
    assinatura = Column(String(64), nullable=False)
    data_hora = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    verificacao = relationship("Verificacao", back_populates="logs")
    relatorio = relationship("Relatorio", back_populates="logs")

    def para_dict(self):
        return {
            "id_log": self.id_log,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "id_verificacao": self.id_verificacao,
            "id_relatorio": self.id_relatorio,
            "assinatura": self.assinatura,
            "data_hora": self.data_hora.isoformat() if self.data_hora else None
        }