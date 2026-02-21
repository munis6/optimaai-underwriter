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


def render_customer_driver_details_page(c, context, page_number=2):
    draw_header_footer(c, page_number)

    usable_width = PAGE_MARGIN_RIGHT - PAGE_MARGIN_LEFT
    y = 700  # Safe top start

    # -----------------------------
    # Title
    # -----------------------------
    title_h = _draw_paragraph(
        c,
        "Customer & Driver Details",
        TITLE_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= title_h + 18  # Updated spacing for global rhythm

    # -----------------------------
    # Customer Information Section
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Customer Information",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 10  # Updated spacing

    # Background card
    c.setFillColor(ACCENT_BG)
    c.roundRect(PAGE_MARGIN_LEFT, y - 90, usable_width, 80, 6, fill=1, stroke=0)

    info_y = y - 15
    app = context.get("applicant", {})

    fields = [
        ("Name:", app.get("name", "")),
        ("ZIP:", app.get("zip", "")),
        ("Address:", app.get("address", "")),
        ("State:", app.get("state", "")),
    ]

    for label, value in fields:
        _draw_paragraph(
            c,
            f"<b>{label}</b> {value}",
            BODY_STYLE,
            PAGE_MARGIN_LEFT + 10,
            info_y,
            usable_width - 20,
        )
        info_y -= 18  # Consistent line spacing

    y -= 100  # Move below card

    # -----------------------------
    # Drivers Section
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Drivers",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 10

    drivers = context.get("drivers", [])

    # Table header
    data = [["Name", "Age", "License Years", "Accidents", "Violations"]]

    # Table rows
    for d in drivers:
        data.append([
            d.get("name", ""),
            d.get("age", ""),
            d.get("licenseYears", ""),
            d.get("accidents", ""),
            d.get("violations", ""),
        ])

    # If no drivers, show one empty row
    if len(drivers) == 0:
        data.append(["N/A", "N/A", "N/A", "N/A", "N/A"])

    # -----------------------------
    # Table Styling (Typography Polish)
    # -----------------------------
    table = Table(
        data,
        colWidths=[usable_width / 5.0] * 5,
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

    c.showPage()
