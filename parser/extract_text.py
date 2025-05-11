
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # adjust if needed

def extract_text_from_pdf(pdf_path: str) -> str:
    pages = convert_from_path(pdf_path, dpi=300)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page) + "\n"
    return text
