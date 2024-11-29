import pandas as pd
import os
def find_last_filled_cell(df, row):
    for col in range(df.shape[1] - 1, -1, -1):
        if not pd.isna(df.iloc[row, col]):
            return df.iloc[row, col]
    return None

def extract_data_from_file(file_path):
    df = pd.read_excel(file_path, sheet_name='Sheet1', header=None)
    
    clientes = df.iloc[4,1]
    ordine = df.iloc[3, 1] if not pd.isna(df.iloc[3, 1]) else None
    capo = df.iloc[3, 12] if not pd.isna(df.iloc[3, 12]) else None
    product_type = df.iloc[4, 12]
    product = df.iloc[3, 12]
    no_of_pieces = df.iloc[9, 6]
    modelo = df.iloc[12,1]
    eficiencia = df.iloc[19, 15]
    
    file_name = os.path.basename(file_path)
    
    total_row = df[df.iloc[:, 0].str.contains('Total', na=False)].index[0]
    total_quantidades = find_last_filled_cell(df, total_row)
    extracted_data = []
    sequencia = 1
    for row in range(29, len(df)):
        if pd.isna(df.iloc[row, 0]):
            break
        
        camada_data = {
            'Nome Arquivo': file_name,
            'clientes': clientes,
            'Ordine': ordine,
            'Capo': capo,
            'Product Type': product_type,
            'Product': product,
            'No. of pieces': no_of_pieces,
            'Modelo': modelo,
            'Total Quantidades': total_quantidades,
            'Eficiencia': eficiencia,
            'Camada': df.iloc[row, 0],
            'Tamanhos no Encaixe': df.iloc[row, 1],
            'Quantidade de Enfesto': df.iloc[row, 3],
            'Tecido': df.iloc[row, 4], 
            'Tipo': df.iloc[row, 5],
            'Largura (cm)': df.iloc[row, 6],
            'Comprimento (m)': df.iloc[row, 7],
            'Tecido Total (m)': df.iloc[row, 8],
            'Consumo Total de tecido (kg)': df.iloc[row, 10],
            'Perímetro de Corte (m)': df.iloc[row, 12],
            'Largura Encolhimento': df.iloc[row, 13],
            'Comprimento Encolhimento': df.iloc[row, 14],
            'Gap de peça (cm)': df.iloc[row, 15],
            'Total de Produtos': df.iloc[row, 16],
            'Numeração do Produto': df.iloc[row, 17],
            'Sequencia': sequencia
        }
        
        if ordine:
            camada_data['Ordine'] = ordine
        if capo:
            camada_data['Capo'] = capo
        
        extracted_data.append(camada_data)
        sequencia += 1
        
    return extracted_data