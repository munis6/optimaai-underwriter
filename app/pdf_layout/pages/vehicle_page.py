from reportlab.lib import colors
from reportlab.platypus import Paragraph

from app.pdf_layout.component.header_footer import draw_header_footer
from app.pdf_layout.style import (
    TITLE_STYLE,
    SECTION_HEADER_STYLE,
    CARD_LABEL_STYLE,
    ACCENT_BG,
    PAGE_MARGIN_LEFT,
    PAGE_MARGIN_RIGHT,
)


def _draw_paragraph(c, text, style, x, y, max_width, max_height=120):
    p = Paragraph(text, style)
    w, h = p.wrap(max_width, max_height)
    p.drawOn(c, x, y - h)
    return h


def render_vehicle_details_page(c, context, page_number=3):
    draw_header_footer(c, page_number)

    usable_width = PAGE_MARGIN_RIGHT - PAGE_MARGIN_LEFT
    y = 700  # Safe top start (consistent with other pages)

    # -----------------------------
    # Title
    # -----------------------------
    title_h = _draw_paragraph(
        c,
        "Vehicle Details",
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
        "Insured Vehicles",
        SECTION_HEADER_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= section_h + 14  # Updated spacing

    # Pull vehicles from context
    vehicles = context.get("vehicles", [])

    # If no vehicles, show 1 empty card
    if len(vehicles) == 0:
        vehicles = [{}]

    # Card layout settings
    card_height = 150
    field_spacing = 18
    top_inner_margin = 16  # Increased for better breathing room

    for v in vehicles:
        # -----------------------------
        # Card Background
        # -----------------------------
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

        # -----------------------------
        # Fields inside card
        # -----------------------------
        line_y = y - top_inner_margin

        fields = [
            ("Year:", v.get("year", "")),
            ("Make:", v.get("make", "")),
            ("Model:", v.get("model", "")),
            ("VIN:", v.get("vin", "")),
            ("Usage:", v.get("usage", "")),
            ("Annual Mileage:", v.get("annualMileage", "")),
            ("Garaging ZIP:", v.get("garagingZip", "")),
        ]

        for label, value in fields:
            _draw_paragraph(
                c,
                f"<b>{label}</b> {value}",
                CARD_LABEL_STYLE,
                PAGE_MARGIN_LEFT + 14,
                line_y,
                usable_width - 28,
            )
            line_y -= field_spacing

        # Space between cards
        y -= card_height + 28  # Slightly increased for cleaner separation

    c.showPage()
