from pathlib import Path
from ocr_module import extract_text
from ai_extractor import extract_invoice_data
from validator import validate_invoice
from storage import save_invoice


def process_document(file_path):
    # استخراج النص من PDF أو صورة
    text = extract_text(file_path)

    if not text.strip():
        print(f"{file_path} -> No text extracted")
        return

    # استخراج بيانات الفاتورة باستخدام AI
    data = extract_invoice_data(text)

    # التحقق من البيانات
    status = validate_invoice(data)

    # حفظ النتيجة
    save_invoice(data, status)

    print(f"{file_path} -> {status}")
    print("Extracted Data:", data)
    print("-" * 50)


if __name__ == "__main__":
    folder = Path("./docs")  # ضع ملفات الفواتير هنا

    if not folder.exists():
        print("❌ Folder 'docs' not found")
    else:
        for file in folder.iterdir():
            if file.suffix.lower() in [".pdf", ".jpg", ".png", ".jpeg", ".webp"]:

                process_document(str(file))

