from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime, timezone

class Relatorio(Base):
    __tablename__ = "relatorios"
    
    id_relatorio = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    formato = Column(String, nullable=False)
    caminho = Column(String, nullable=False)
    criado_por = Column(String, default="api")
    id_verificacao = Column(Integer, ForeignKey('verificacoes.id_verificacao', ondelete="CASCADE"), nullable=False)
    data_hora = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    logs = relationship("Log", back_populates="relatorio", lazy="joined", cascade="all, delete-orphan")
    verificacao = relationship("Verificacao", back_populates="relatorios", lazy="joined")

    def para_dict(self):
        return {
            "id_relatorio": self.id_relatorio,
            "tipo": self.tipo,
            "formato": self.formato,
            "caminho": self.caminho,
            "criado_por": self.criado_por,
            "id_verificacao": self.id_verificacao,
            "data_hora": self.data_hora.isoformat() if self.data_hora else None
        }