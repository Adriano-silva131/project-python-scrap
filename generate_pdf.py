from reportlab.lib.pagesizes import A6, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def generate_pdf(ordem, camadas, logo_path):
    try:
        # Verificar se `camadas` é uma lista ou uma única instância
        if not isinstance(camadas, list):
            camadas = [camadas]  # Transforma em uma lista com um único elemento se for uma instância

        # Iterar sobre cada camada para gerar um PDF separado
        for idx, camada in enumerate(camadas):
            # Caminho onde o PDF será salvo
            file_name = f"sequencia_corte_ordem_{ordem.ordem}_camada_{idx+1}.pdf"
            
            # Criar o PDF com o tamanho A6 e em landscape (paisagem)
            c = canvas.Canvas(file_name, pagesize=landscape(A6))
            
            # Configurar algumas propriedades
            width, height = landscape(A6)  # Obtemos as dimensões da página já rotacionada
            c.setTitle("Sequência / Corte")
            
            # Inserir logo no cabeçalho
            if logo_path:
                c.drawImage(logo_path, 1.5 * cm, height - 2.2 * cm, width=2.5 * cm, height=1.5 * cm, mask='auto')

            # Cabeçalho
            c.setFont("Helvetica-Bold", 16)  # Ajuste o tamanho da fonte para A6
            c.drawString(5 * cm, height - 1.8 * cm, f"SEQUÊNCIA / CORTE")

            # Adicionar mais espaçamento e ajustar o layout
            vertical_spacing = 1 * cm
            field_height = 1 * cm

            # Informações da Ordem - Pedido
            c.rect(1.5 * cm, height - 3.5 * cm, 11 * cm, field_height)
            c.setFont("Helvetica", 10)
            c.drawString(1.7 * cm, height - 3.2 * cm, f"OP- Pedido: {ordem.ordem}")

            # Informações do Tecido/Cor
            c.rect(1.5 * cm, height - 4.5 * cm, 11 * cm, field_height)
            c.drawString(1.7 * cm, height - 4.2 * cm, f"Tecido/Cor: {camada.tecido}")
            
            # Largura (cm)
            c.rect(1.5 * cm, height - 5.5 * cm, 11 * cm, field_height)
            c.drawString(1.7 * cm, height - 5.2 * cm, f"Largura (cm): {camada.largura_cm}")

            # Tipo
            c.rect(1.5 * cm, height - 6.5 * cm, 11 * cm, field_height)
            c.drawString(1.7 * cm, height - 6.2 * cm, f"Tipo: {camada.tipo}")

            # Cabeçalho da Tabela de Detalhes da Camada
            c.setFont("Helvetica-Bold", 9)
            # Desenhar o cabeçalho da tabela com divisões bem espaçadas
            c.drawString(1.7 * cm, height - 7.7 * cm, "Seq")
            c.drawString(3 * cm, height - 7.7 * cm, "Qtde de Folhas")
            c.drawString(5 * cm, height - 7.7 * cm, "Compri. Enfesto")
            c.drawString(7 * cm, height - 7.7 * cm, "Qtd tecido")
            c.drawString(9 * cm, height - 7.7 * cm, "Itens por Folha")

            # Linha da tabela para os dados
            y_position = height - 8.2 * cm  # Ajuste da posição vertical
            c.rect(1.5 * cm, y_position, 11 * cm, field_height)  # Retângulo para linha de dados

            # Desenhar os dados nas respectivas colunas com espaçamento adequado
            c.setFont("Helvetica", 9)
            c.drawString(1.7 * cm, y_position + 0.2 * cm, f"{idx+1}")  # Coluna Seq
            c.drawString(3 * cm, y_position + 0.2 * cm, f"{camada.quantidade_enfesto}")  # Coluna Qtde de Folhas
            c.drawString(5 * cm, y_position + 0.2 * cm, f"{camada.comprimento_m}")  # Coluna Compri. Enfesto
            c.drawString(7 * cm, y_position + 0.2 * cm, f"{camada.tecido_total_m}")  # Coluna Qtd tecido
            c.drawString(9 * cm, y_position + 0.2 * cm, f"{camada.tamanhos_no_encaixe}")  # Coluna Itens por Folha
            
            # Salvar o PDF
            c.showPage()
            c.save()
            
            print(f"PDF gerado: {file_name}")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o PDF: {e}")
