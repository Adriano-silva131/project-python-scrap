from reportlab.lib.pagesizes import A6, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from services.directory_save import load_output_directory
import os

def generate_pdf(ordem, camadas, logo_path):
    try:
        output_dir = load_output_directory()

        if not output_dir:
            output_dir = "."

        if not isinstance(camadas, list):
            camadas = [camadas]

        for idx, camada in enumerate(camadas):
            file_name = os.path.join(output_dir, f"sequencia_corte_ordem_{ordem.nome_arquivo}_sequencia_{camada.sequencia}.pdf")
            c = canvas.Canvas(file_name, pagesize=landscape(A6))
            width, height = landscape(A6)
            c.setTitle("Sequência / Corte")

            # Inserir a logo
            if logo_path:
                c.drawImage(
                    logo_path,
                    1 * cm,
                    height - 1.5 * cm,
                    width=2 * cm,
                    height=1.2 * cm,
                    mask="auto",
                )

            # Cabeçalho (com fonte menor)
            c.setFont("Helvetica-Bold", 10)  # Fonte reduzida
            c.drawString(4.5 * cm, height - 1 * cm, f"SEQUÊNCIA / CORTE")

            # Dados da ordem
            data = [
                ["OP - Pedido:", f"{ordem.ordem}"],
                ["Cliente:", f"{ordem.clientes}"],
                ["Tecido/Cor:", f"{camada.tecido}"],
                ["Largura (cm):", f"{camada.largura_cm}"],
                ["Item:", f"{ordem.product}"],
                ["Lado:", f"{ordem.product_type}"],
            ]

            # Tabela de dados da ordem
            table = Table(
                data, colWidths=[4.5 * cm, 7.5 * cm], rowHeights=[0.5 * cm] * len(data)
            )
            table.setStyle(
                TableStyle(
                    [
                        ("FONT", (0, 0), (-1, -1), "Helvetica", 8),  # Fonte reduzida
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (0, -1), "LEFT"),
                        ("ALIGN", (1, 0), (1, -1), "CENTER"),
                    ]
                )
            )

            # Posicionar a tabela (subida para o topo)
            table.wrapOn(c, width, height)
            table.drawOn(c, 1 * cm, height - 4.5 * cm)

            # Dados da camada
            data_camada = [
                ["Seq", f"{camada.sequencia}"],
                ["Qtde de Folhas", f"{camada.quantidade_enfesto}"],
                ["Comprimento Enfesto", f"{camada.comprimento_m}"],
                ["Qtd tecido", f"{camada.tecido_total_m}"],
                ["Itens por Folha", f"{camada.tamanhos_no_encaixe}"],
            ]

            # Tabela de dados da camada
            table_camada = Table(
                data_camada,
                colWidths=[4.5 * cm, 7.5 * cm],
                rowHeights=[0.5 * cm] * len(data_camada),
            )
            table_camada.setStyle(
                TableStyle(
                    [
                        ("FONT", (0, 0), (-1, -1), "Helvetica", 7),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ]
                )
            )

            # Posicionar a tabela da camada (mais próxima do cabeçalho)
            table_camada.wrapOn(c, width, height)
            table_camada.drawOn(c, 1 * cm, height - 8.5 * cm)

            c.showPage()
            c.save()
            print(f"PDF gerado: {file_name}")
            print(f"Gerando PDFs no diretório: {output_dir}")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o PDF: {e}")
