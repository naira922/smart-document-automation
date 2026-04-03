from pathlib import Path
from ocr_module import extract_text
from ai_extractor import extract_invoice_data
from validator import validate_invoice
from storage import save_invoice


def process_document(file_path):

    text = extract_text(file_path)

    if not text.strip():
        print(f"{file_path} -> No text extracted")
        return

   
    data = extract_invoice_data(text)

   
    status = validate_invoice(data)

    
    save_invoice(data, status)

    print(f"{file_path} -> {status}")
    print("Extracted Data:", data)
    print("-" * 50)


if __name__ == "__main__":
    folder = Path("./docs")  #

    if not folder.exists():
        print(" Folder 'docs' not found")
    else:
        for file in folder.iterdir():
            if file.suffix.lower() in [".pdf", ".jpg", ".png", ".jpeg", ".webp"]:

                process_document(str(file))

