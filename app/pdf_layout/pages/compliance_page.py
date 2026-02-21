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


def _draw_paragraph(c, text, style, x, y, max_width, max_height=140):
    p = Paragraph(text, style)
    w, h = p.wrap(max_width, max_height)
    p.drawOn(c, x, y - h)
    return h


def render_compliance_summary_page(c, context, page_number=6):
    draw_header_footer(c, page_number)

    usable_width = PAGE_MARGIN_RIGHT - PAGE_MARGIN_LEFT
    y = 700  # Safe top start

    # -----------------------------
    # Extract compliance data
    # -----------------------------
    compliance = context.get("compliance", {})
    state = compliance.get("state", "N/A")
    overall = compliance.get("overallStatus", "N/A")
    notes = compliance.get("notes", "N/A")
    rules = compliance.get("rulesChecked", [])
    narrative = compliance.get("narrative", "")

    # -----------------------------
    # Title
    # -----------------------------
    title_h = _draw_paragraph(
        c,
        "Compliance Summary",
        TITLE_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= title_h + 18  # Updated spacing

    # -----------------------------
    # Top Fields
    # -----------------------------
    fields = [
        ("State:", state),
        ("Overall Status:", overall),
        ("Notes:", notes),
    ]

    for label, value in fields:
        y -= _draw_paragraph(
            c,
            f"<b>{label}</b> {value}",
            BODY_STYLE,
            PAGE_MARGIN_LEFT,
            y,
            usable_width,
        ) + 10

    y -= 12  # Extra breathing room

    # -----------------------------
    # Rules Checked Section
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Rules Checked",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 12

    # Table header
    data = [["Rule ID", "Description", "Passed", "Severity"]]

    # Populate rows
    for r in rules:
        data.append([
            r.get("ruleId", ""),
            r.get("description", ""),
            "Yes" if r.get("passed", False) else "No",
            r.get("severity", ""),
        ])

    # Fallback if no rules
    if len(rules) == 0:
        data.append(["N/A", "N/A", "N/A", "N/A"])

    # -----------------------------
    # Table Styling (Typography Polish)
    # -----------------------------
    table = Table(
        data,
        colWidths=[
            usable_width * 0.15,
            usable_width * 0.45,
            usable_width * 0.15,
            usable_width * 0.25,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                # Header
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
    # Compliance Narrative
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Compliance Narrative",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 12

    # Narrative card background
    c.setFillColor(ACCENT_BG)
    c.roundRect(
        PAGE_MARGIN_LEFT,
        y - 100,
        usable_width,
        100,
        6,
        fill=1,
        stroke=0,
    )

    line_y = y - 20

    # Render up to 3 lines of narrative
    for line in narrative.split("\n")[:3]:
        _draw_paragraph(
            c,
            line if line else " ",
            BODY_STYLE,
            PAGE_MARGIN_LEFT + 12,
            line_y,
            usable_width - 24,
        )
        line_y -= 18

    c.showPage()
