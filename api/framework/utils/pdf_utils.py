import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_content):
    """
    Extracts all text from a PDF file.

    Args:
        pdf_content (bytes): The binary content of the PDF file.

    Returns:
        str: A string containing the extracted text from the entire PDF document.
    """
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    text = "".join(page.get_text() for page in pdf_document)
    pdf_document.close()
    return text
