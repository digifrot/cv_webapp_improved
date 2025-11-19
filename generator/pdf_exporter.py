# generator/pdf_exporter.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

from generator.config import LINKEDIN_PROFILE
import re


def save_pdf(text, filename, job_title="CV"):
    """Generate a nicely formatted PDF from a plain-text CV string with working hyperlinks."""
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        title=f"Liran Roth - {job_title}",
        author="Liran Roth",
        subject="CV"
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
            fontSize=16,
            fontName="Helvetica-Bold",
            allowHTML=True,
            leading=18,
            alignment=TA_LEFT,
            underlineProportion=0.1,
            linkUnderline=True,   
            textColor=colors.HexColor("#0C2B4E"),           # <-- CRITICAL for clickable hyperlinks
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
    current_section = None

    for line in lines[1:]:
        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 8))

        elif stripped.isupper() and len(stripped) < 60:
            # SECTION TITLES (SUMMARY, EXPERIENCE, SKILLS...)
            story.append(Paragraph(f"<b>{stripped}</b>", styles["Section"]))
            # Track current section so we can add special formatting to its
            # body (e.g., bold job titles inside EXPERIENCE)
            current_section = stripped.upper()
        elif stripped.upper() == "EXPERIENCE":
            # Support case-insensitive 'Experience' (not uppercase) in case
            # the base CV is formatted differently.
            story.append(Paragraph(f"<b>{stripped}</b>", styles["Section"]))
            current_section = "EXPERIENCE"

        else:
            # Normal body paragraph
            # If we are inside an EXPERIENCE section, identify lines that
            # look like job title lines and make them bold. Heuristic:
            # - contain a pipe '|' plus a 4-digit year OR
            # - contain a 4-digit year at the end of the line
            is_job_title = False
            if current_section == "EXPERIENCE":
                # Look for patterns like: "Head of... | 2022 - 2025" or
                # "Role | 2019" - most CV job title lines include a year
                # or a '|' separator before the company/time
                if ("|" in stripped and re.search(r"\b\d{4}\b", stripped)):
                    is_job_title = True
                elif re.search(r"\b\d{4}\b\s*-\s*\d{4}\b", stripped):
                    is_job_title = True

            if is_job_title:
                story.append(Paragraph(f"<b>{stripped}</b>", styles["Body"]))
            else:
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
