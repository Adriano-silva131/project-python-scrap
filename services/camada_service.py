from sqlalchemy.orm import Session
from models.camada_model import Camada


def cria_camada(db: Session, ordem_id: int, camada_data: dict):
    camada_existente = db.query(Camada).filter_by(
        camada=camada_data.get('camada'),
        ordem_id = ordem_id,
        tamanhos_no_encaixe=camada_data.get('tamanhos_no_encaixe'),
        quantidade_enfesto=camada_data.get('quantidade_enfesto'),
        tecido=camada_data.get('tecido'),
        largura_cm=camada_data.get('largura_cm'),
        comprimento_m=camada_data.get('comprimento_m'),
        total_de_produtos=camada_data.get('total_de_produtos'),
        numeracao_do_produto=camada_data.get('numeracao_do_produto'),
    ).first()
    
    if camada_existente:
        return camada_existente
    
    camada = Camada(ordem_id=ordem_id, **camada_data)
    db.add(camada)
    db.commit()
    return camada