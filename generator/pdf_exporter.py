# generator/pdf_exporter.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

from generator.config import LINKEDIN_PROFILE


def save_pdf(text, filename):
    """Generate a nicely formatted PDF from a plain-text CV string with working hyperlinks."""
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40
    )

    styles = getSampleStyleSheet()

    # Base body style
    styles.add(
        ParagraphStyle(
            name="Body",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.black
        )
    )

    # Header style with hyperlink support
    styles.add(
        ParagraphStyle(
            name="Header",
            fontSize=11,
            allowHTML=True,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.black,
            underlineProportion=0.1,
            linkUnderline=True,              # <-- CRITICAL for clickable hyperlinks
        )
    )

    # Section titles
    styles.add(
        ParagraphStyle(
            name="Section",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#222222"),
            spaceAfter=8,
        )
    )

    story = []

    # --- Split into lines
    lines = text.splitlines()
    if not lines:
        doc.build(story)
        return

    # --- HEADER (first line ONLY)
    header = lines[0].strip()
    if header:
        story.append(Paragraph(_ensure_link_in_header(header), styles["Header"]))
        story.append(Spacer(1, 12))

    # --- BODY (rest of CV)
    for line in lines[1:]:
        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 8))

        elif stripped.isupper() and len(stripped) < 60:
            # SECTION TITLES (SUMMARY, EXPERIENCE, SKILLS...)
            story.append(Paragraph(f"<b>{stripped}</b>", styles["Section"]))

        else:
            # Normal body paragraph
            story.append(Paragraph(stripped, styles["Body"]))

    # --- Build PDF
    doc.build(story)


def _ensure_link_in_header(header_line: str) -> str:
    """Ensure the LinkedIn portion of the header is rendered as a clickable link."""
    if "<link" in header_line:
        return header_line

    link_markup = f"<link href='{LINKEDIN_PROFILE}'>LinkedIn</link>"

    if "LinkedIn" in header_line:
        return header_line.replace("LinkedIn", link_markup, 1)

    separator = "" if header_line.endswith(" | ") else " | "
    return f"{header_line}{separator}{link_markup}"
