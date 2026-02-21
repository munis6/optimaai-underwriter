# risk_narrative.py

from ai_narratives.tone_controller import apply_tone_control


def generate_risk_narrative(data: dict) -> str:
    """
    Generates a clean, regulator-safe risk narrative
    based on normalized JSON fields and underwriting signals.
    """
    inputs = extract_risk_inputs(data)

    risk_factors = summarize_risk_factors(inputs["risk_factors"])
    positive_factors = summarize_positive_factors(inputs["positive_factors"])

    summary = build_risk_summary(
        inputs["risk_score"],
        inputs["risk_level"],
        risk_factors,
        positive_factors
    )

    return apply_tone_control(assemble_risk_narrative(summary))

def extract_risk_inputs(data: dict) -> dict:
    """
    Extracts all fields needed for the risk narrative.
    """
    return {
        "risk_score": data.get("riskScore"),
        "risk_level": data.get("riskLevel"),
        "risk_factors": data.get("riskFactors", {}),
        "positive_factors": data.get("positiveFactors", {}),
    }


def summarize_risk_factors(risk_factors: dict) -> list:
    """
    Converts risk factor fields into readable phrases.
    """
    results = []
    for key, value in risk_factors.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def summarize_positive_factors(positive_factors: dict) -> list:
    """
    Converts positive underwriting factors into readable phrases.
    """
    results = []
    for key, value in positive_factors.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def build_risk_summary(risk_score, risk_level, risk_factors, positive_factors):
    """
    Builds the core sentence fragments used in the final risk narrative.
    """
    return {
        "score": (
            f"The AI-assigned risk score for this submission is {risk_score}."
            if risk_score is not None else ""
        ),
        "level": (
            f"This places the submission in the '{risk_level}' risk tier."
            if risk_level else ""
        ),
        "risk_factors": (
            f"Key risk drivers include: {', '.join(risk_factors)}."
            if risk_factors else "No elevated risk factors were identified."
        ),
        "positive_factors": (
            f"Positive underwriting indicators include: {', '.join(positive_factors)}."
            if positive_factors else "No positive underwriting indicators were noted."
        ),
    }


def assemble_risk_narrative(summary: dict) -> str:
    """
    Combines all sentence fragments into a clean, regulator-safe narrative.
    """
    parts = [
        summary.get("score", ""),
        summary.get("level", ""),
        summary.get("risk_factors", ""),
        summary.get("positive_factors", "")
    ]

    return " ".join([p for p in parts if p])
