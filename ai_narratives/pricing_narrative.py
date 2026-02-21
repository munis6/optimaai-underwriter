# pricing_narrative.py

from ai_narratives.tone_controller import apply_tone_control

def generate_pricing_narrative(data: dict) -> str:
    """
    Generates a clean, regulator-safe pricing narrative
    based on normalized JSON fields.
    """
    inputs = extract_pricing_inputs(data)

    surcharge_list = summarize_surcharges(inputs["surcharges"])
    discount_list = summarize_discounts(inputs["discounts"])

    summary = build_pricing_summary(
        inputs["base_premium"],
        inputs["total_premium"],
        surcharge_list,
        discount_list
    )

    return apply_tone_control(assemble_pricing_narrative(summary))

def extract_pricing_inputs(data: dict) -> dict:
    """
    Extracts all fields needed for the pricing narrative.
    This keeps the narrative generator clean and modular.
    """
    return {
        "base_premium": data.get("base_premium"),
        "total_premium": data.get("total_premium"),
        "surcharges": data.get("surcharges", {}),
        "discounts": data.get("discounts", {}),
        "risk_score": data.get("risk_score"),
    }


def summarize_surcharges(surcharges: dict) -> list:
    """
    Converts surcharge fields into short human-readable phrases.
    """
    results = []
    for key, value in surcharges.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def summarize_discounts(discounts: dict) -> list:
    """
    Converts discount fields into short human-readable phrases.
    """
    results = []
    for key, value in discounts.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def build_pricing_summary(base_premium, total_premium, surcharge_list, discount_list):
    """
    Builds the core sentence fragments used in the final pricing narrative.
    """
    return {
        "base": f"The base premium for this policy is ${base_premium:.2f}." if base_premium else "",
        "total": f"The total premium is ${total_premium:.2f} after adjustments." if total_premium else "",
        "surcharges": (
            f"Surcharges applied include: {', '.join(surcharge_list)}."
            if surcharge_list else "No surcharges were applied."
        ),
        "discounts": (
            f"Discounts applied include: {', '.join(discount_list)}."
            if discount_list else "No discounts were applied."
        ),
    }


def assemble_pricing_narrative(summary: dict) -> str:
    """
    Combines all sentence fragments into a clean, regulator-safe narrative.
    """
    parts = [
        summary.get("base", ""),
        summary.get("total", ""),
        summary.get("surcharges", ""),
        summary.get("discounts", "")
    ]

    # Join non-empty parts with spaces
    return " ".join([p for p in parts if p])
