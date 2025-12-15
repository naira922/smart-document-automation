import pytesseract
from PIL import Image
import PyPDF2
from pdf2image import convert_from_path
import os

def extract_text(file_path, original_name=None, poppler_path=None):
    """
    Extract text from PDF or image file.

    Parameters:
    - file_path: path to the temporary file
    - original_name: original filename (used to detect extension)
    - poppler_path: path to Poppler bin folder (optional, for PDF OCR)
    """
    # Use original filename to detect extension if given
    if original_name:
        file_ext = original_name.split('.')[-1].lower()
    else:
        file_ext = file_path.split('.')[-1].lower()

    text = ""

    if file_ext == "pdf":
        try:
            # Try to extract text directly first
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            # If no text found, fallback to OCR
            if not text.strip():
                pages = convert_from_path(file_path, poppler_path=poppler_path)
                for page in pages:
                    text += pytesseract.image_to_string(page) + "\n"

        except Exception as e:
            text = f"Error processing PDF: {e}"

    elif file_ext in ["jpg", "jpeg", "png", "webp"]:
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
        except Exception as e:
            text = f"Error processing image: {e}"

    else:
        raise ValueError(f"Unsupported file type: {original_name or file_path}")

    return text







