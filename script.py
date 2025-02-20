import os
import pandas as pd

# Caminho do diretório contendo os arquivos
directory_path = "planilhas"

# Lista para armazenar todos os dados extraídos
all_data = []


# Função para encontrar a última célula preenchida em uma linha
def find_last_filled_cell(df, row):
    for col in range(df.shape[1] - 1, -1, -1):
        if not pd.isna(df.iloc[row, col]):
            return df.iloc[row, col]
    return None


# Percorrer todos os arquivos no diretório
for filename in os.listdir(directory_path):
    if filename.endswith(".xls"):
        file_path = os.path.join(directory_path, filename)

        # Carregar a planilha
        df = pd.read_excel(file_path, sheet_name="Sheet1", header=None)

        # Extraindo os dados fixos
        ordine = df.iloc[3, 1]
        cliente = df.iloc[4, 1]
        capo = df.iloc[3, 12]
        no_of_pieces = df.iloc[9, 6]
        eficiencia = df.iloc[19, 15]
        spread = df.iloc[20, 4]

        total_row = df[df.iloc[:, 0].str.contains("Total", na=False)].index[0]
        total_quantidades = find_last_filled_cell(df, total_row)

        for row in range(29, len(df)):
            if pd.isna(df.iloc[row, 0]):
                break

            camada_data = {
                "Ordine": ordine,
                "Cliente": cliente,
                "Capo": capo,
                "spread": spread,
                "No. of pieces": no_of_pieces,
                "Total Quantidades": total_quantidades,
                "Eficiencia": eficiencia,
                "Camada": df.iloc[row, 0],
                "Tamanhos no Encaixe": df.iloc[row, 1],
                "Camadas": f"{df.iloc[row, 3]}, {df.iloc[row, 4]}",
                "Tipo": df.iloc[row, 5],
                "Largura (cm)": df.iloc[row, 6],
                "Comprimento (m)": df.iloc[row, 7],
                "Tecido Total (m)": f"{df.iloc[row, 8]}, {df.iloc[row, 9]}",
                "Consumo Total de tecido (kg)": f"{df.iloc[row, 10]}, {df.iloc[row, 11]}",
                "Perímetro de Corte (m)": df.iloc[row, 12],
                "Largura Encolhimento": df.iloc[row, 13],
                "Comprimento Encolhimento": df.iloc[row, 14],
                "Gap de peça (cm)": df.iloc[row, 15],
                "Total de Produtos": df.iloc[row, 16],
                "Numeração do Produto": df.iloc[row, 17],
            }
            all_data.append(camada_data)

df_all_data = pd.DataFrame(all_data)

output_file_path = "consolidado.xlsx"
df_all_data.to_excel(output_file_path, index=False)

print(f"Dados consolidados salvos em: {output_file_path}")
