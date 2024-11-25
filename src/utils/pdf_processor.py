import pdfplumber
from src.models.summary_model import get_summary_json

def process_pdf(pdf_path):
    script_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            script_text += page.extract_text()
    return get_summary_json(script_text)
