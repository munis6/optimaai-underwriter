from reportlab.lib import colors
from reportlab.platypus import Paragraph

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


def render_ai_insights_summary_page(c, context, page_number=7):
    draw_header_footer(c, page_number)

    usable_width = PAGE_MARGIN_RIGHT - PAGE_MARGIN_LEFT
    y = 700  # Safe top start

    # -----------------------------
    # Extract AI insights
    # -----------------------------
    ai = context.get("aiInsights", {})

    driver = ai.get("driverRiskFactors", "")
    pricing = ai.get("pricingRationale", "")
    explanation = ai.get("underwritingExplanation", "")
    suggestions = ai.get("improvementSuggestions", "")
    narrative = ai.get("narrative", "")

    sections = [
        ("Driver Risk Factors", driver),
        ("Pricing Rationale", pricing),
        ("Underwriting Explanation", explanation),
        ("Improvement Suggestions", suggestions),
        ("AI Narrative", narrative),
    ]

    # -----------------------------
    # Title
    # -----------------------------
    title_h = _draw_paragraph(
        c,
        "AI Insights Summary",
        TITLE_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    )
    y -= title_h + 18  # Updated spacing

    # -----------------------------
    # Render each section
    # -----------------------------
    for label, value in sections:

        # Section header
        section_h = _draw_paragraph(
            c,
            label,
            SECTION_HEADER_STYLE,
            PAGE_MARGIN_LEFT,
            y,
            usable_width,
        )
        y -= section_h + 12  # Updated spacing

        # Background card
        card_height = 90
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

        # Render up to 3 lines of text
        line_y = y - 20
        lines = value.split("\n") if value else ["", "", ""]
        for line in lines[:3]:
            _draw_paragraph(
                c,
                line if line else " ",
                BODY_STYLE,
                PAGE_MARGIN_LEFT + 12,
                line_y,
                usable_width - 24,
            )
            line_y -= 18

        y -= card_height + 28  # Premium spacing between sections

    c.showPage()
