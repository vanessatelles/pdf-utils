import PyPDF2
import os

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

if __name__ == "__main__":
    input_pdf = "14.1_A_paginas_extraidas.pdf"
    pages_to_rotate = [1]  # Pages to rotate (1-based indexing)

    try:
        output_pdf = rotate_pdf_pages(input_pdf, pages_to_rotate, -90)
        print(f"PDF successfully processed. Output saved to: {output_pdf}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
