from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
os.makedirs("proposals", exist_ok=True)

# ---- MAIN FUNCTION ----
def generate_proposal_pdf(lead, ai_summary, file_path):
    """
    Generates a clean, corporate-style PDF proposal for SunQuote AI.
    """
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # SunQuote AI Brand Colors
    BLUE = colors.HexColor("#1A73E8")
    YELLOW = colors.HexColor("#FFB300")
    DARK = colors.HexColor("#1F2937")

    # ---------------------
    # PAGE 1 — EXEC SUMMARY
    # ---------------------
    c.setFillColor(BLUE)
    c.rect(0, height - 80, width, 80, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(40, height - 45, "SUNQUOTE AI")

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, height - 120, "Solar Proposal Summary")

    c.setFont("Helvetica", 12)
    y = height - 160

    # Customer details
    customer_lines = [
        f"Customer Name: {lead.get('customer_name', '')}",
        f"Email: {lead.get('email', '')}",
        f"Phone: {lead.get('phone', '')}",
        f"Address: {lead.get('address', '')}",
        f"Property Type: {lead.get('property_type', '')}",
        f"Estimated System Size: {lead.get('system_size_kw', '')} kW",
        f"Average Monthly Bill: ₹{lead.get('avg_monthly_bill', '')}",
        f"Utility Provider: {lead.get('utility', 'N/A')}",
    ]

    for line in customer_lines:
        c.drawString(40, y, line)
        y -= 20

    # Highlight box: Estimated Cost (placeholder values)
    c.setFillColor(colors.white)
    c.setStrokeColor(BLUE)
    c.rect(40, y - 60, 250, 60, stroke=1, fill=0)

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 25, "Estimated Project Cost:")
    c.setFont("Helvetica", 13)
    c.drawString(50, y - 45, "₹1,10,000 – ₹1,75,000")

    c.showPage()

    # ---------------------
    # PAGE 2 — TECHNICAL OVERVIEW
    # ---------------------
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 50, "Technical Overview")

    c.setFont("Helvetica", 12)
    tech_data = [
        "• Expected Annual Energy Production: 4200–6000 kWh",
        "• Expected Annual Savings: ₹22,000 – ₹38,000",
        "• System Output Degradation: ~0.5% per year",
        "• Estimated Payback: 3.5 – 5.2 years",
        "• Panel Warranty: 25 years (performance)",
        "• Inverter Warranty: 5–10 years",
    ]

    y = height - 100
    for line in tech_data:
        c.drawString(40, y, line)
        y -= 22

    c.showPage()

    # ---------------------
    # PAGE 3 — AI SUMMARY
    # ---------------------
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 50, "AI-Generated Summary")

    c.setFont("Helvetica", 12)
    text = c.beginText(40, height - 90)
    text.setLeading(18)

    ai_text = ai_summary or "No AI summary available."

    for line in ai_text.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.showPage()

    # ---------------------
    # PAGE 4 — BRAND INFO
    # ---------------------
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(BLUE)
    c.drawString(40, height - 50, "SunQuote AI")

    c.setFillColor(DARK)
    c.setFont("Helvetica", 12)
    branding_text = [
        "SunQuote AI is your intelligent solar sales assistant.",
        "This proposal was automatically generated using AI.",
        "",
        "Support: support@sunquote.ai",
        "Website: www.sunquote.ai",
    ]

    y = height - 100
    for line in branding_text:
        c.drawString(40, y, line)
        y -= 20

    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.grey)
    c.drawString(40, 40, "Disclaimer: Cost and production values are estimated and may vary.")

    c.save()
    return file_path
