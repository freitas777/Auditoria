from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime, timezone

class Verificacao(Base):
    __tablename__ = "verificacoes"
    
    id_verificacao = Column(Integer, primary_key=True, index=True)
    id_voto = Column(String(36), nullable=False)
    comprovante = Column(Text, nullable=False)
    resultado = Column(Boolean, nullable=False)
    mensagem = Column(String, nullable=False)
    criado_por = Column(String, default="api")
    data_hora = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    logs = relationship("Log", back_populates="verificacao", lazy="joined", cascade="all, delete-orphan")
    relatorios = relationship("Relatorio", back_populates="verificacao", lazy="joined", cascade="all, delete-orphan")

    def para_dict(self):
        return {
            "id_verificacao": self.id_verificacao,
            "id_voto": self.id_voto,
            "comprovante": self.comprovante,
            "resultado": self.resultado,
            "mensagem": self.mensagem,
            "criado_por": self.criado_por,
            "data_hora": self.data_hora.isoformat() if self.data_hora else None
        }