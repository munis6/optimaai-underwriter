from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle

from app.pdf_layout.component.header_footer import draw_header_footer
from app.pdf_layout.style import (
    TITLE_STYLE,
    SECTION_HEADER_STYLE,
    BODY_STYLE,
    MICRO_STYLE,
    ACCENT_BG,
    PAGE_MARGIN_LEFT,
    PAGE_MARGIN_RIGHT,
)


def _draw_paragraph(c, text, style, x, y, max_width, max_height=120):
    p = Paragraph(text, style)
    w, h = p.wrap(max_width, max_height)
    p.drawOn(c, x, y - h)
    return h


def render_coverage_summary_page(c, context, page_number=4):
    draw_header_footer(c, page_number)

    usable_width = PAGE_MARGIN_RIGHT - PAGE_MARGIN_LEFT
    y = 700  # Safe top start

    # -----------------------------
    # Title
    # -----------------------------
    title_h = _draw_paragraph(
        c,
        "Coverage Summary",
        TITLE_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= title_h + 18  # Updated spacing

    # -----------------------------
    # Selected Coverages Section
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Selected Coverages",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 12  # Updated spacing

    # Pull coverage list
    coverages = context.get("coverage", [])

    # Table header
    data = [["Coverage Type", "Limit", "Deductible", "Included"]]

    # Populate rows
    for cov in coverages:
        data.append([
            cov.get("type", ""),
            cov.get("limit", ""),
            cov.get("deductible", ""),
            "Yes" if cov.get("included", False) else "No",
        ])

    # If no coverages, show one empty row
    if len(coverages) == 0:
        data.append(["N/A", "N/A", "N/A", "N/A"])

    # -----------------------------
    # Table Styling (Typography Polish)
    # -----------------------------
    table = Table(
        data,
        colWidths=[
            usable_width * 0.35,
            usable_width * 0.2,
            usable_width * 0.2,
            usable_width * 0.25,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                # Header row
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2A4B8D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "SourceSans3-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),

                # Body rows
                ("FONTNAME", (0, 1), (-1, -1), "SourceSans3"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#000000")),

                # Alignment
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                # Row striping
                ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                 [colors.white, colors.HexColor("#F5F5F5")]),

                # Grid
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
            ]
        )
    )

    tw, th = table.wrap(usable_width, 200)
    table.drawOn(c, PAGE_MARGIN_LEFT, y - th)
    y -= th + 28  # Increased spacing for premium rhythm

    # -----------------------------
    # Full Coverage Indicator
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Full Coverage Indicator",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 10

    full_cov = context.get("fullCoverageIndicator", "N/A")

    y -= _draw_paragraph(
        c,
        f"{full_cov}",
        BODY_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    ) + 20

    # -----------------------------
    # Coverage Narrative
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Coverage Narrative",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 12

    narrative = context.get("coverageNarrative", "")

    # Narrative card background
    c.setFillColor(ACCENT_BG)
    c.roundRect(PAGE_MARGIN_LEFT, y - 100, usable_width, 100, 6, fill=1, stroke=0)

    line_y = y - 20

    # Render up to 3 lines of narrative
    for line in narrative.split("\n")[:3]:
        _draw_paragraph(
            c,
            line,
            BODY_STYLE,
            PAGE_MARGIN_LEFT + 12,
            line_y,
            usable_width - 24,
        )
        line_y -= 18

    c.showPage()
