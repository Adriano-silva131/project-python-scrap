from services.ordem_service import cria_ordem
from services.camada_service import cria_camada
from sqlalchemy.orm import Session


def insert_data_to_db(db: Session, data):
    for entry in data:
        ordem = cria_ordem(db, {
            'ordem': str(entry['Ordine']),
            'numero_pecas': entry['No. of pieces'],
            'quantidade_total': entry['Total Quantidades'],
            'product_type': entry['Product Type'],
            'eficiencia': entry['Eficiencia'],
            'nome_arquivo': entry['Nome Arquivo']
        })
        
        cria_camada(db, ordem.id, {
            'camada': entry['Camada'],
            'tamanhos_no_encaixe': entry['Tamanhos no Encaixe'],
            'quantidade_enfesto': entry['Quantidade de Enfesto'],
            'tecido': entry['Tecido'],
            'tipo': entry['Tipo'],
            'largura_cm': entry['Largura (cm)'],
            'comprimento_m': entry['Comprimento (m)'],
            'tecido_total_m': entry['Tecido Total (m)'],
            'consumo_total_tecido_kg': entry['Consumo Total de tecido (kg)'],
            'perimetro_de_corte_m': entry['Perímetro de Corte (m)'],
            'largura_encolhimento': entry['Largura Encolhimento'],
            'comprimento_encolhimento': entry['Comprimento Encolhimento'],
            'gap_de_peca_cm': entry['Gap de peça (cm)'],
            'total_de_produtos': entry['Total de Produtos'],
            'numeracao_do_produto': entry['Numeração do Produto']
        })