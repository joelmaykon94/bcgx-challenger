import PyPDF2
from io import BytesIO

def extract_text_from_pdf(content: bytes) -> str:
    text = ""
    with BytesIO(content) as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

    return text
