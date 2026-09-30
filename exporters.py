from datetime import datetime
from pathlib import Path
from fpdf import FPDF
from .config import EXPORTS_DIR

def save_pdf(layout):
    filename = f"comiccraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = EXPORTS_DIR / filename

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 10, f"Panel {panel['panel_number']}: {panel['title']}")
        pdf.ln(3)

        image_path = Path(panel["image_path"])
        if image_path.exists():
            pdf.image(str(image_path), x=15, y=35, w=180)
            pdf.ln(120)

        pdf.set_font("Helvetica", "I", 11)
        pdf.multi_cell(0, 7, panel["scene_description"])
        pdf.ln(3)

        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 7, "Caption")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, panel["caption"])
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 7, "Narration / Dialogue")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, panel["narration"])
        if panel.get("dialogue"):
            pdf.ln(2)
            pdf.multi_cell(0, 7, panel["dialogue"])

    pdf.output(str(path))
    return str(path)
