import csv
from pathlib import Path

def save_invoice(data, status, csv_file="invoices_output.csv"):
    """
    Save invoice data with validation status to a CSV file.
    """
    file_path = Path(csv_file)
    # إذا الملف مش موجود، أضف header
    if not file_path.exists():
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(data.keys()) + ["status"])
            writer.writeheader()
    
    # أضف بيانات الفاتورة
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(data.keys()) + ["status"])
        row = data.copy()
        row["status"] = status
        writer.writerow(row)

