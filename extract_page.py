from PyPDF2 import PdfReader, PdfWriter

def extrair_paginas_pdf(caminho_entrada, caminho_saida, paginas):
    """
    Extrai páginas específicas de um PDF e salva em outro PDF.

    :param caminho_entrada: Caminho do arquivo PDF original
    :param caminho_saida: Caminho para salvar o novo PDF
    :param paginas: Lista de páginas a extrair (índices baseados em 1)
    """
    reader = PdfReader(caminho_entrada)
    writer = PdfWriter()

    # Converte para índice baseado em zero e remove páginas inválidas
    total_paginas = len(reader.pages)
    paginas_validas = [p - 1 for p in paginas if 1 <= p <= total_paginas]

    if not paginas_validas:
        print("Nenhuma página válida para extrair.")
        return

    for pagina in paginas_validas:
        writer.add_page(reader.pages[pagina])

    with open(caminho_saida, "wb") as f_out:
        writer.write(f_out)

    print(f"Novo PDF salvo em: {caminho_saida}")


