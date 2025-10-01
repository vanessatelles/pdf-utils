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


if __name__ == "__main__":
    # Exemplo de uso:
    extrair_paginas_pdf(
        "/content/DFS_001.PDF",
        "/content/paginas_extraidas.pdf",
        paginas_para_extrair
    )

    paginas_para_extrair = [1,2,3,4, 6, 9, 11, 14, 19, 32, 56, 86, 90, 94]  # base 1

    # Exemplo de uso 2:
    paginas_para_extrair_2 = [
        11, 14,
        *range(18, 287),
        *range(287, 299),
        *range(302, 312),
        *range(313, 316),
        *range(317, 320),
        *range(629, 774),
        *range(775, 956)
    ]

    extrair_paginas_pdf(
        "/content/KD7-001_B.pdf",
        "/content/paginas_extraidas_2.pdf",
        paginas_para_extrair_2
    )