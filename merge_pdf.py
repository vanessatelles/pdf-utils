from PyPDF2 import PdfMerger
import os

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
        if os.path.exists(pdf):
            merger.append(pdf)
        else:
            print(f"Warning: File {pdf} not found")

    # Write the merged PDF to the output path
    merger.write(output_path)
    merger.close()

    print(f"PDFs merged successfully! Output saved to: {output_path}")

