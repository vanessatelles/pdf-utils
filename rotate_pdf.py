import PyPDF2
import os
import argparse
import sys

def rotate_pdf_pages(input_pdf_path, pages_to_rotate, degrees, output_pdf_path=None):
    """
    Rotate specific pages in a PDF file by 90 degrees clockwise.

    Args:
        input_pdf_path (str): Path to the input PDF file
        pages_to_rotate (list): List of page numbers to rotate (1-based indexing)
        output_pdf_path (str, optional): Path for the output PDF file. If not provided,
                                       will create a new file with '_rotated' suffix
    """
    # If no output path is provided, create one based on the input path
    if output_pdf_path is None:
        base_name = os.path.splitext(input_pdf_path)[0]
        output_pdf_path = f"{base_name}_rotated.pdf"

    # Open the input PDF file
    with open(input_pdf_path, 'rb') as file:
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        # Create PDF writer object
        pdf_writer = PyPDF2.PdfWriter()

        # Process each page
        for page_num in range(len(pdf_reader.pages)):
            # Get the page
            page = pdf_reader.pages[page_num]

            # If this page should be rotated (page_num + 1 because of 0-based indexing)
            if (page_num + 1) in pages_to_rotate:
                # Rotate the page x degrees clockwise
                page.rotate(degrees)

            # Add the page to the writer
            pdf_writer.add_page(page)

        # Write the modified PDF to the output file
        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer.write(output_file)

    return output_pdf_path

def parse_paginas(paginas_str):
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
    parser = argparse.ArgumentParser(description="Rotaciona páginas específicas de um PDF")
    parser.add_argument("-i", "--input", required=True, help="Caminho do PDF de entrada")
    parser.add_argument("-o", "--output", required=False, help="Caminho do PDF de saída")
    parser.add_argument(
        "-p", "--paginas", required=True,
        help="Páginas a rotacionar (ex: 1,2,5-8) - base 1"
    )
    parser.add_argument(
        "-d", "--degrees", type=int, required=True,
        help="Graus para rotacionar (positivos = horário, negativos = anti-horário), múltiplos de 90"
    )
    args = parser.parse_args()

    if args.degrees % 90 != 0:
        print("Graus deve ser múltiplo de 90.")
        sys.exit(1)

    paginas = parse_paginas(args.paginas)
    if not paginas:
        print("Nenhuma página válida informada.")
        sys.exit(1)

    output = rotate_pdf_pages(args.input, paginas, args.degrees, args.output)
    print(f"PDF processado com sucesso. Salvo em: {output}")
