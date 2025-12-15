import pypdf

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrae texto de un archivo PDF.
    """
    text = ""
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
    return text
