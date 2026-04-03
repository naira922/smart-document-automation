def validate_invoice(data):
    """
    Validate invoice data.
    Returns:
        "approved" if total_amount < 5000,
        "needs_review" if total_amount >= 5000,
        "rejected" if required fields are missing
    """

    required_fields = ["invoice_number", "invoice_date", "vendor_name", "total_amount", "currency"]
    for field in required_fields:
        if not data.get(field):
            return "rejected"

    
    try:
        amount = float(data.get("total_amount", 0))
    except:
        return "rejected"

    if amount < 5000:
        return "approved"
    else:
        return "needs_review"


