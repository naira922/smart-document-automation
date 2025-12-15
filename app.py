import streamlit as st
import tempfile
from pathlib import Path
from ocr_module import extract_text
from ai_extractor import extract_invoice_data
from validator import validate_invoice
import csv

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="Smart Document Automation",
    layout="centered",
    page_icon="📄",
    initial_sidebar_state="expanded"
)

st.title("📄 Smart Document Automation")
st.write("Upload one or more invoices (PDF or Image) to extract structured data")

# ----------------- CSV Storage -----------------
csv_file = Path("processed_invoices.csv")
if not csv_file.exists():
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["invoice_number", "invoice_date", "vendor_name", "total_amount", "currency", "status"])
        writer.writeheader()

# ----------------- File Upload -----------------
uploaded_files = st.file_uploader(
    "📤 Upload invoices",
    type=["pdf", "jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

# ----------------- Process Files -----------------
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.divider()
        st.subheader(f"📎 File: {uploaded_file.name}")

        # Save file temporarily with correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            tmp.write(uploaded_file.read())
            file_path = tmp.name

        # OCR Step
        try:
            with st.spinner("🔍 Extracting text..."):
                text = extract_text(file_path)
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
            continue

        # Show OCR Text
        st.subheader("🧾 OCR Output")
        st.text_area("Extracted Text", text, height=220)

        if not text.strip():
            st.error("❌ No text could be extracted from this file")
            continue

        # AI Extraction Step
        try:
            with st.spinner("🤖 Analyzing invoice..."):
                data = extract_invoice_data(text)
                status = validate_invoice(data)
                data["status"] = status
        except Exception as e:
            st.error(f"❌ Error extracting invoice data: {e}")
            continue

        # Show Results
        st.success("✅ Invoice processed successfully")
        st.subheader("📊 Extracted Structured Data")
        st.json(data)
        st.subheader("📌 Validation Status")
        st.write(status)

        # Save to CSV
        try:
            with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["invoice_number", "invoice_date", "vendor_name", "total_amount", "currency", "status"])
                writer.writerow(data)
        except Exception as e:
            st.error(f"❌ Error saving to CSV: {e}")

    # ----------------- CSV Download -----------------
    if csv_file.exists():
        with open(csv_file, "rb") as f:
            st.download_button(
                label="💾 Download Processed CSV",
                data=f,
                file_name="processed_invoices.csv",
                mime="text/csv"
            )

else:
    st.info("👆 Please upload one or more invoice files to start")









