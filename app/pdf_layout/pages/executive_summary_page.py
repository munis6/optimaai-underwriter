from reportlab.platypus import Paragraph
from app.pdf_layout.component.header_footer import draw_header_footer, draw_divider
from app.pdf_layout.style import (
    TITLE_STYLE,
    SECTION_HEADER_ACCENT,
    BODY_STYLE,
    MICRO_STYLE,
    PAGE_MARGIN_LEFT,
    PAGE_MARGIN_RIGHT,
)


def _draw_paragraph(c, text, style, x, y, max_width, max_height=200):
    p = Paragraph(text, style)
    w, h = p.wrap(max_width, max_height)
    p.drawOn(c, x, y - h)
    return h


def _risk_score_insight(score, state):
    if not isinstance(score, (int, float)):
        return ""

    if score >= 80:
        tier = "Preferred"
    elif score >= 60:
        tier = "Standard‑Preferred"
    elif score >= 40:
        tier = "Standard"
    else:
        tier = "High‑Risk"

    return f"Risk score of {score} places this applicant in the <b>{tier}</b> tier for {state}."


def _premium_insight(premium):
    try:
        p = float(premium)
    except:
        return ""

    if p < 800:
        return "Premium is lower than typical for similar profiles."
    elif p <= 1500:
        return "Premium is within the expected range for similar profiles."
    else:
        return "Premium is higher than typical for similar profiles."


def render_executive_summary_page(c, context, page_number=1):
    draw_header_footer(c, page_number)

    usable_width = PAGE_MARGIN_RIGHT - PAGE_MARGIN_LEFT
    y = 700  # Safe top start

    # -----------------------------
    # Title
    # -----------------------------
    y -= _draw_paragraph(
        c,
        "Executive Summary",
        TITLE_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    ) + 18  # Updated spacing

    applicant = context.get("applicant", {})
    summary = context.get("summary", {})
    risk = context.get("risk", {})
    pricing = context.get("pricing", {})

    # -----------------------------
    # Applicant Summary Section
    # -----------------------------
    fields = [
        ("Applicant Name:", applicant.get("name", "")),
        ("State:", applicant.get("state", "")),
        ("Risk Score:", f"<b>{risk.get('score', '')}</b>"),
        ("Eligibility Decision:", risk.get("eligibility", "")),
        ("Premium:", pricing.get("finalPremium", "")),
    ]

    for label, value in fields:
        line = f"<b>{label}</b> {value}"
        y -= _draw_paragraph(
            c,
            line,
            BODY_STYLE,
            PAGE_MARGIN_LEFT,
            y,
            usable_width,
        ) + 8

        # Micro‑insights under Risk Score and Premium
        if label == "Risk Score:":
            insight = _risk_score_insight(risk.get("score"), applicant.get("state"))
            if insight:
                y -= _draw_paragraph(
                    c,
                    insight,
                    MICRO_STYLE,
                    PAGE_MARGIN_LEFT,
                    y,
                    usable_width,
                ) + 6

        if label == "Premium:":
            insight = _premium_insight(pricing.get("finalPremium"))
            if insight:
                y -= _draw_paragraph(
                    c,
                    insight,
                    MICRO_STYLE,
                    PAGE_MARGIN_LEFT,
                    y,
                    usable_width,
                ) + 6

    # Divider line with more breathing room
    y -= 16
    draw_divider(c, y)
    y -= 24

    # -----------------------------
    # Top 3 Risk Drivers
    # -----------------------------
    y -= _draw_paragraph(
        c,
        "Top 3 Risk Drivers",
        SECTION_HEADER_ACCENT,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    ) + 10

    risk_drivers = risk.get("topDrivers", [])[:3] or ["N/A"]

    for i, item in enumerate(risk_drivers, start=1):
        y -= _draw_paragraph(
            c,
            f"{i}. {item}",
            BODY_STYLE,
            PAGE_MARGIN_LEFT,
            y,
            usable_width,
        ) + 6

    # Divider
    y -= 16
    draw_divider(c, y)
    y -= 24

    # -----------------------------
    # Top 3 Pricing Factors
    # -----------------------------
    y -= _draw_paragraph(
        c,
        "Top 3 Pricing Factors",
        SECTION_HEADER_ACCENT,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    ) + 10

    pricing_factors = pricing.get("topPricingFactors", [])[:3] or ["N/A"]

    for i, item in enumerate(pricing_factors, start=1):
        y -= _draw_paragraph(
            c,
            f"{i}. {item}",
            BODY_STYLE,
            PAGE_MARGIN_LEFT,
            y,
            usable_width,
        ) + 6

    # Divider
    y -= 16
    draw_divider(c, y)
    y -= 24

    # -----------------------------
    # Summary Narrative
    # -----------------------------
    y -= _draw_paragraph(
        c,
        "Summary Narrative",
        SECTION_HEADER_ACCENT,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    ) + 10

    narrative = summary.get("narrative", "No narrative provided.")
    y -= _draw_paragraph(
        c,
        narrative.replace("\n", "<br/>"),
        BODY_STYLE,
        PAGE_MARGIN_LEFT,
        y,
        usable_width,
    ) + 20

    c.showPage()
