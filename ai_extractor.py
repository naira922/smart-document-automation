import google.generativeai as genai
import json
import re

# Configure your API key
genai.configure(api_key="AIzaSyC6TOqwMnSE1fe8TT1rA2-maMJqtl2iAwM")  # استبدلي بالمفتاح بتاعك

MODEL_NAME = "gemini-2.5-flash"  # تأكدي إن الموديل موجود

model = genai.GenerativeModel(MODEL_NAME)

def extract_invoice_data(text):
    """
    Extract structured invoice data using AI with regex fallback
    """
    # ----------------- AI Prompt -----------------
    prompt = f"""
Extract the following fields from the invoice text:
- invoice_number
- invoice_date
- vendor_name
- total_amount
- currency

If a field is missing, return null.
Return **only valid JSON**.

Invoice Text:
{text}

Respond only in JSON format.
"""

    try:
        response = model.generate_content(prompt)
        data = json.loads(response.text)
    except:
        # إذا AI رجع حاجة مش JSON
        data = {
            "invoice_number": None,
            "invoice_date": None,
            "vendor_name": None,
            "total_amount": None,
            "currency": None
        }

    # ----------------- Regex Fallback -----------------
    if not data.get("invoice_number"):
        match = re.search(r"Order ID\s*:\s*([A-Z0-9\-]+)", text)
        data["invoice_number"] = match.group(1) if match else None

    if not data.get("total_amount"):
        amounts = re.findall(r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?", text)
        if amounts:
            # نفترض آخر قيمة هي المجموع الكلي
            data["total_amount"] = float(amounts[-1].replace('$','').replace(',',''))

    if not data.get("invoice_date"):
        match = re.search(r"([A-Z][a-z]{2,}\s\d{1,2}\s\d{4})", text)
        data["invoice_date"] = match.group(1) if match else None

    if not data.get("vendor_name"):
        match = re.search(r"Bill To\s*:\s*(.*)", text)
        data["vendor_name"] = match.group(1).strip() if match else None

    if not data.get("currency") and data.get("total_amount"):
        data["currency"] = "USD"  # افتراض الدولار، ممكن تعدلي حسب الحاجة

    return data


