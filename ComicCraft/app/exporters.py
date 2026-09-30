from datetime import datetime
from pathlib import Path
from fpdf import FPDF

from .config import EXPORTS_DIR


def clean_text(text):
    """Convert AI text into safe PDF text."""

    if text is None:
        return ""

    text = str(text)

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
        "\n": "\n",
        "\r": "\n",
        "\t": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove unsupported characters
    text = text.encode("latin-1", "replace").decode("latin-1")

    return text


def break_long_words(text, max_length=30):
    """
    Break very long continuous words so FPDF
    can wrap them correctly.
    """

    if not text:
        return ""

    lines = text.split("\n")
    fixed_lines = []

    for line in lines:

        words = line.split(" ")
        new_words = []

        for word in words:

            if len(word) > max_length:

                parts = [
                    word[i:i + max_length]
                    for i in range(
                        0,
                        len(word),
                        max_length
                    )
                ]

                new_words.append(" ".join(parts))

            else:
                new_words.append(word)

        fixed_lines.append(" ".join(new_words))

    return "\n".join(fixed_lines)


def safe_text(text):
    """Prepare text safely for FPDF."""

    text = clean_text(text)

    text = break_long_words(
        text,
        max_length=30
    )

    return text


def write_text(pdf, text, height=7):
    """
    Safely write text inside the PDF.
    """

    text = safe_text(text)

    if not text:
        return

    pdf.multi_cell(
        180,
        height,
        text
    )


def save_pdf(layout):

    filename = (
        "comiccraft_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        + ".pdf"
    )

    path = EXPORTS_DIR / filename

    # Make sure export folder exists
    EXPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in layout:

        pdf.add_page()

        # ==================================
        # PANEL TITLE
        # ==================================

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        title = (
            "Panel "
            + str(panel.get("panel_number", ""))
            + ": "
            + str(panel.get("title", ""))
        )

        write_text(
            pdf,
            title,
            10
        )

        pdf.ln(3)

        # ==================================
        # PANEL IMAGE
        # ==================================

        image_path = Path(
            panel.get("image_path", "")
        )

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=15,
                y=35,
                w=180
            )

            pdf.ln(120)

        # ==================================
        # SCENE DESCRIPTION
        # ==================================

        pdf.set_font(
            "Helvetica",
            "I",
            11
        )

        scene = panel.get(
            "scene_description",
            ""
        )

        write_text(
            pdf,
            scene,
            7
        )

        pdf.ln(3)

        # ==================================
        # CAPTION
        # ==================================

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        write_text(
            pdf,
            "Caption",
            7
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        caption = panel.get(
            "caption",
            ""
        )

        write_text(
            pdf,
            caption,
            7
        )

        pdf.ln(2)

        # ==================================
        # NARRATION
        # ==================================

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        write_text(
            pdf,
            "Narration / Dialogue",
            7
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        narration = panel.get(
            "narration",
            ""
        )

        write_text(
            pdf,
            narration,
            7
        )

        # ==================================
        # DIALOGUE
        # ==================================

        dialogue = panel.get(
            "dialogue",
            ""
        )

        if dialogue:

            pdf.ln(2)

            write_text(
                pdf,
                dialogue,
                7
            )

    # ==================================
    # SAVE PDF
    # ==================================

    pdf.output(
        str(path)
    )

    print(
        "PDF CREATED:",
        str(path)
    )

    return str(path)