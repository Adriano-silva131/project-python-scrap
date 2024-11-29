from sqlalchemy.orm import Session
from models.ordem_model import Ordem

def cria_ordem(db: Session, ordem_data: dict):
    ordem_existente = db.query(Ordem).filter_by(
        ordem=ordem_data.get('ordem'),
        numero_pecas=ordem_data.get('numero_pecas'),
        quantidade_total=ordem_data.get('quantidade_total'),
        nome_arquivo=ordem_data.get('nome_arquivo')
    ).first()
    
    if ordem_existente:
        return ordem_existente
    
    ordem = Ordem(**ordem_data)
    db.add(ordem)
    db.commit()
    db.refresh(ordem)
    return ordem