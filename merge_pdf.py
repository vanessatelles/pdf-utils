from PyPDF2 import PdfMerger, PdfReader
import os
import argparse

def is_valid_pdf(file_path):
    """
    Check if a file is a valid PDF.

    Args:
        file_path (str): Path to the PDF file

    Returns:
        bool: True if file is a valid PDF, False otherwise
    """
    try:
        with open(file_path, 'rb') as file:
            PdfReader(file)
        return True
    except Exception as e:
        print(f"Error validating PDF {file_path}: {str(e)}")
        return False

def merge_pdfs(file_list, output_path):
    """
    Merge multiple PDF files into a single PDF.

    Args:
        file_list (list): List of PDF file paths to merge
        output_path (str): Path where the merged PDF will be saved
    """
    # Create a PDF merger object
    merger = PdfMerger()

    # Add each PDF to the merger
    for pdf in file_list:
        if not os.path.exists(pdf):
            print(f"Warning: File {pdf} not found")
            continue

        if not is_valid_pdf(pdf):
            print(f"Warning: {pdf} is not a valid PDF file")
            continue

        try:
            merger.append(pdf)
            print(f"Successfully added {pdf}")
        except Exception as e:
            print(f"Error processing {pdf}: {str(e)}")
            continue

    if merger.getNumPages() == 0:
        print("No valid PDFs were found to merge!")
        return

    try:
        # Write the merged PDF to the output path
        merger.write(output_path)
        merger.close()
        print(f"PDFs merged successfully! Output saved to: {output_path}")
    except Exception as e:
        print(f"Error saving merged PDF: {str(e)}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mescla múltiplos PDFs em um único arquivo")
    parser.add_argument(
        "-i", "--inputs", nargs='+', required=True,
        help="Lista de caminhos de PDFs a serem mesclados (ordem importa)"
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Caminho do PDF de saída"
    )
    args = parser.parse_args()

    merge_pdfs(args.inputs, args.output)