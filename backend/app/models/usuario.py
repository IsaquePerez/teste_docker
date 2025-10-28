from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    nivel_acesso_id = Column(Integer, ForeignKey("niveis_acesso.id"), nullable=False)
    ativo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamento
    nivel_acesso = relationship("NivelAcesso", back_populates="usuarios", foreign_keys=[nivel_acesso_id])
    projetos_responsavel = relationship("Projeto", back_populates="responsavel", foreign_keys="[Projeto.responsavel_id]")
    tentativas = relationship("RegistroTentativaTeste", back_populates="usuario", foreign_keys="[RegistroTentativaTeste.usuario_id]")