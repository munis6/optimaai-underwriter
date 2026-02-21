# eligibility_narrative.py

from ai_narratives.tone_controller import apply_tone_control

def generate_eligibility_narrative(data: dict) -> str:
    """
    Generates a clean, regulator-safe eligibility narrative
    based on underwriting and compliance signals.
    """
    inputs = extract_eligibility_inputs(data)

    reasons = summarize_eligibility_reasons(inputs["eligibility_reasons"])
    blockers = summarize_blockers(inputs["blockers"])

    summary = build_eligibility_summary(
        inputs["eligibility"],
        reasons,
        blockers
    )

    return apply_tone_control(assemble_eligibility_narrative(summary))

def extract_eligibility_inputs(data: dict) -> dict:
    """
    Extracts all fields needed for the eligibility narrative.
    """
    return {
        "eligibility": data.get("eligibility"),
        "eligibility_reasons": data.get("eligibilityReasons", {}),
        "blockers": data.get("eligibilityBlockers", {}),
    }


def summarize_eligibility_reasons(reasons: dict) -> list:
    """
    Converts eligibility reasons into readable phrases.
    """
    results = []
    for key, value in reasons.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def summarize_blockers(blockers: dict) -> list:
    """
    Converts eligibility blockers into readable phrases.
    """
    results = []
    for key, value in blockers.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def build_eligibility_summary(eligibility, reasons, blockers):
    """
    Builds the core sentence fragments used in the final eligibility narrative.
    """
    return {
        "eligibility": (
            f"The applicant is classified as '{eligibility}' for this submission."
            if eligibility else ""
        ),
        "reasons": (
            f"Eligibility is supported by: {', '.join(reasons)}."
            if reasons else "No specific eligibility-supporting factors were identified."
        ),
        "blockers": (
            f"Eligibility blockers include: {', '.join(blockers)}."
            if blockers else "No eligibility blockers were identified."
        ),
    }


def assemble_eligibility_narrative(summary: dict) -> str:
    """
    Combines all sentence fragments into a clean, regulator-safe narrative.
    """
    parts = [
        summary.get("eligibility", ""),
        summary.get("reasons", ""),
        summary.get("blockers", "")
    ]

    return " ".join([p for p in parts if p])
