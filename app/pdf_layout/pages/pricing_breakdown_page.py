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


def render_pricing_breakdown_page(c, context, page_number=5):
    draw_header_footer(c, page_number)

    usable_width = PAGE_MARGIN_RIGHT - PAGE_MARGIN_LEFT
    y = 700  # Safe top start

    # -----------------------------
    # Title
    # -----------------------------
    title_h = _draw_paragraph(
        c,
        "Pricing Breakdown",
        TITLE_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= title_h + 18  # Updated spacing for global rhythm

    # -----------------------------
    # Section Header
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Premium Components",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 14  # Updated spacing

    # Extract pricing data
    pricing = context.get("pricing", {})

    base = pricing.get("basePremium", "N/A")
    driver = pricing.get("driverImpact", "N/A")
    vehicle = pricing.get("vehicleImpact", "N/A")
    zip_impact = pricing.get("zipImpact", "N/A")
    coverage = pricing.get("coverageImpact", "N/A")
    discounts = pricing.get("discounts", "N/A")

    # -----------------------------
    # Left-side Bar Chart Placeholder Card
    # -----------------------------
    chart_width = usable_width * 0.45
    chart_height = 130

    c.setFillColor(ACCENT_BG)
    c.roundRect(
        PAGE_MARGIN_LEFT,
        y - chart_height,
        chart_width,
        chart_height,
        6,
        fill=1,
        stroke=0,
    )

    _draw_paragraph(
        c,
        "Bar Chart Placeholder (Base, Driver, Vehicle, ZIP, Coverage, Discounts)",
        BODY_STYLE,
        PAGE_MARGIN_LEFT + 12,
        y - 12,
        chart_width - 24,
    )

    # -----------------------------
    # Table on the Right Side
    # -----------------------------
    table_x = PAGE_MARGIN_LEFT + chart_width + 20
    table_width = usable_width - chart_width - 20

    data = [
        ["Component", "Amount"],
        ["Base Premium:", base],
        ["Driver Impact:", driver],
        ["Vehicle Impact:", vehicle],
        ["ZIP Impact:", zip_impact],
        ["Coverage Impact:", coverage],
        ["Discounts/Surcharges:", discounts],
    ]

    table = Table(
        data,
        colWidths=[table_width * 0.65, table_width * 0.35],
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

    tw, th = table.wrap(table_width, 200)
    table.drawOn(c, table_x, y - th)

    y -= max(chart_height, th) + 32  # Increased spacing for premium rhythm

    # -----------------------------
    # Pricing Narrative
    # -----------------------------
    section_h = _draw_paragraph(
        c,
        "Pricing Narrative",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 12

    narrative = pricing.get("narrative", "")

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
