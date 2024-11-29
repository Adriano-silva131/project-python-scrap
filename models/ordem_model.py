from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from config.database import Base

class Ordem(Base):
    __tablename__ = "ordens"
    id = Column(Integer, primary_key=True, index=True)
    ordem = Column(String)
    numero_pecas = Column(Integer)
    product_type = Column(String)
    quantidade_total = Column(Integer)
    eficiencia = Column(String)
    nome_arquivo = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    clientes = Column(String)
    product = Column(String)
    
    camadas = relationship("Camada", back_populates="ordem")
