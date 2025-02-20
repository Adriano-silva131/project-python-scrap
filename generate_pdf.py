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

        file_name = os.path.join(
            output_dir, f"sequencia_corte_ordem_{ordem.nome_arquivo}.pdf"
        )
        c = canvas.Canvas(file_name, pagesize=landscape(A6))
        width, height = landscape(A6)
        c.setTitle("Sequência / Corte")

        for idx, camada in enumerate(camadas):
            if logo_path:
                c.drawImage(
                    logo_path,
                    1 * cm,
                    height - 1.5 * cm,
                    width=2 * cm,
                    height=1.2 * cm,
                    mask="auto",
                )

            c.setFont("Helvetica-Bold", 10)
            c.drawString(4.5 * cm, height - 1 * cm, f"SEQUÊNCIA / CORTE")

            data = [
                ["OP - Pedido:", f"{ordem.ordem}"],
                ["Cliente:", f"{ordem.clientes}"],
                ["Tecido/Cor:", f"{camada.tecido}"],
                ["Largura (cm):", f"{camada.largura_cm}"],
                ["Item:", f"{ordem.product}"],
                ["Lado:", f"{ordem.product_type}"],
            ]

            table = Table(
                data, colWidths=[6.5 * cm, 7.0 * cm], rowHeights=[0.5 * cm] * len(data)
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

            table.wrapOn(c, width, height)
            table.drawOn(c, 1 * cm, height - 4.5 * cm)

            data_camada = [
                ["Seq", f"{camada.sequencia}"],
                ["Qtde de Folhas", f"{camada.quantidade_enfesto}"],
                ["Comprimento Enfesto", f"{camada.comprimento_m}"],
                [
                    "Qtd tecido",
                    str(
                        round(
                            (
                                float(str(camada.spread).replace(",", ".")) * 2
                                + float(str(camada.comprimento_m).replace(",", "."))
                            )
                            * float(str(camada.quantidade_enfesto).replace(",", ".")),
                            2,  # Número de casas decimais
                        )
                    ),
                ],
                ["Itens por Folha", f"{camada.tamanhos_no_encaixe}"],
            ]

            table_camada = Table(
                data_camada,
                colWidths=[6.5 * cm, 7.0 * cm],
                rowHeights=[0.6 * cm] * len(data_camada),
            )
            table_camada.setStyle(
                TableStyle(
                    [
                        ("FONT", (0, 0), (-1, -1), "Helvetica", 8),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ]
                )
            )

            table_camada.wrapOn(c, width, height)
            table_camada.drawOn(c, 1 * cm, height - 8.5 * cm)

            c.showPage()

        c.save()
        print(f"PDF único gerado: {file_name}")
        print(f"Gerando PDFs no diretório: {output_dir}")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o PDF: {e}")
