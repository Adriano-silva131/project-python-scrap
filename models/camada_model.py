from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Camada(Base):
    __tablename__ = "camadas"

    id = Column(Integer, primary_key=True, index=True)
    ordem_id = Column(Integer, ForeignKey('ordens.id'))
    camada = Column(String)
    tamanhos_no_encaixe = Column(String)
    quantidade_enfesto = Column(String)
    tecido = Column(String)
    tipo = Column(String)
    largura_cm = Column(String)
    comprimento_m = Column(String)
    tecido_total_m = Column(String)
    consumo_total_tecido_kg = Column(String)
    perimetro_de_corte_m = Column(String)
    largura_encolhimento = Column(String)
    comprimento_encolhimento = Column(String)
    gap_de_peca_cm = Column(String)
    total_de_produtos = Column(Integer)
    numeracao_do_produto = Column(String)
    
    
    ordem = relationship("Ordem", back_populates="camadas")