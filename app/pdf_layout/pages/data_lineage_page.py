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


def render_data_lineage_page(c, context, page_number=8):
    draw_header_footer(c, page_number)

    usable_width = PAGE_MARGIN_RIGHT - PAGE_MARGIN_LEFT
    y = 700  # Safe top start

    # -----------------------------
    # Extract lineage data
    # -----------------------------
    lineage = context.get("lineage", [])

    # -----------------------------
    # Title
    # -----------------------------
    title_h = _draw_paragraph(
        c,
        "Data Lineage & Field Traceability",
        TITLE_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= title_h + 18  # Updated spacing

    # -----------------------------
    # Field-Level Lineage Section
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Field-Level Lineage",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 12

    # Table header
    data = [["Field Name", "Source System", "Source Path", "Normalized Path Inferred"]]

    # Populate rows
    if isinstance(lineage, list) and len(lineage) > 0:
        for item in lineage:
            if isinstance(item, dict):
                data.append([
                    item.get("fieldName", ""),
                    item.get("sourceSystem", ""),
                    item.get("sourcePath", ""),
                    item.get("normalizedPath", ""),
                ])
            else:
                # Fallback for non-dict entries
                data.append([str(item), "N/A", "N/A", "N/A"])
    else:
        data.append(["N/A", "N/A", "N/A", "N/A"])

    # -----------------------------
    # Table Styling (Typography Polish)
    # -----------------------------
    table = Table(
        data,
        colWidths=[
            usable_width * 0.2,
            usable_width * 0.2,
            usable_width * 0.3,
            usable_width * 0.3,
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
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),

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
    y -= th + 28  # Premium spacing

    # -----------------------------
    # Missing Data Summary
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Missing Data Summary",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 12

    # Background card
    card_height = 100
    c.setFillColor(ACCENT_BG)
    c.roundRect(
        PAGE_MARGIN_LEFT,
        y - card_height,
        usable_width,
        card_height,
        6,
        fill=1,
        stroke=0,
    )

    # Render 3 placeholder lines
    line_y = y - 20
    for _ in range(3):
        _draw_paragraph(
            c,
            "__________________________________________________",
            BODY_STYLE,
            PAGE_MARGIN_LEFT + 12,
            line_y,
            usable_width - 24,
        )
        line_y -= 18

    c.showPage()
