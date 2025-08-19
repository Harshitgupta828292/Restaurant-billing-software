from fpdf import FPDF
from io import BytesIO

def generate_simple_pdf(purchase_date, cart, total_amount, gst_amount, payment_mode):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", size=16)
    pdf.cell(0, 10, "Restaurant Bill", ln=True, align="C")

    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, f"Purchase Date: {purchase_date.strftime('%d-%m-%Y')}", ln=True)
    pdf.cell(0, 10, f"Payment Mode: {payment_mode}", ln=True)
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(80, 10, "Item", border=1)
    pdf.cell(30, 10, "Qty", border=1)
    pdf.cell(40, 10, "Price", border=1)
    pdf.cell(40, 10, "Total", border=1, ln=True)

    pdf.set_font("Helvetica", size=12)
    for item in cart.values():
        item_total = item['price'] * item['qty']
        pdf.cell(80, 10, item['name'], border=1)
        pdf.cell(30, 10, str(item['qty']), border=1)
        pdf.cell(40, 10, f"{item['price']:.2f}", border=1)
        pdf.cell(40, 10, f"{item_total:.2f}", border=1, ln=True)

    subtotal = total_amount - gst_amount
    pdf.cell(150, 10, "Subtotal", border=1)
    pdf.cell(40, 10, f"{subtotal:.2f}", border=1, ln=True)

    pdf.cell(150, 10, "GST (5%)", border=1)
    pdf.cell(40, 10, f"{gst_amount:.2f}", border=1, ln=True)

    pdf.cell(150, 10, "Total", border=1)
    pdf.cell(40, 10, f"{total_amount:.2f}", border=1, ln=True)

    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_output)
    buffer.seek(0)
    return buffer
