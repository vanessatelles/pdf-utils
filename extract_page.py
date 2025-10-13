from PyPDF2 import PdfReader, PdfWriter
import argparse
import sys

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


def parse_paginas(paginas_str):
    # Suporta formatos como "1,2,5-8,10"
    paginas = []
    if not paginas_str:
        return paginas
    for parte in paginas_str.split(','):
        parte = parte.strip()
        if not parte:
            continue
        if '-' in parte:
            try:
                inicio, fim = parte.split('-', 1)
                inicio = int(inicio)
                fim = int(fim)
                if inicio <= fim:
                    paginas.extend(list(range(inicio, fim + 1)))
                else:
                    paginas.extend(list(range(fim, inicio + 1)))
            except ValueError:
                print(f"Ignorando intervalo inválido: {parte}")
        else:
            try:
                paginas.append(int(parte))
            except ValueError:
                print(f"Ignorando página inválida: {parte}")
    # Remove duplicatas preservando ordem
    seen = set()
    paginas_unicas = []
    for p in paginas:
        if p not in seen:
            paginas_unicas.append(p)
            seen.add(p)
    return paginas_unicas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrai páginas específicas de um PDF")
    parser.add_argument("-i", "--input", required=True, help="Caminho do PDF de entrada")
    parser.add_argument("-o", "--output", required=True, help="Caminho do PDF de saída")
    parser.add_argument(
        "-p", "--paginas", required=True,
        help="Páginas a extrair (ex: 1,2,5-8) - base 1"
    )
    args = parser.parse_args()

    paginas = parse_paginas(args.paginas)
    if not paginas:
        print("Nenhuma página válida informada.")
        sys.exit(1)

    extrair_paginas_pdf(args.input, args.output, paginas)