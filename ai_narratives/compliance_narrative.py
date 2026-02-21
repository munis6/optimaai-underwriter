# compliance_narrative.py

from ai_narratives.tone_controller import apply_tone_control

def generate_compliance_narrative(data: dict) -> str:
    """
    Generates a clean, regulator-safe compliance narrative
    based on normalized JSON fields and underwriting flags.
    """
    inputs = extract_compliance_inputs(data)

    violations_list = summarize_violations(inputs["violations"])
    missing_items_list = summarize_missing_items(inputs["missing_items"])

    summary = build_compliance_summary(
        violations_list,
        missing_items_list,
        inputs["state"],
        inputs["eligibility"]
    )

    return apply_tone_control(assemble_compliance_narrative(summary))


def extract_compliance_inputs(data: dict) -> dict:
    """
    Extracts all fields needed for the compliance narrative.
    """
    return {
        "state": data.get("state"),
        "eligibility": data.get("eligibility"),
        "violations": data.get("complianceViolations", {}),
        "missing_items": data.get("missingComplianceItems", {}),
    }


def summarize_violations(violations: dict) -> list:
    """
    Converts compliance violation fields into readable phrases.
    """
    results = []
    for key, value in violations.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def summarize_missing_items(missing_items: dict) -> list:
    """
    Converts missing compliance items into readable phrases.
    """
    results = []
    for key, value in missing_items.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def build_compliance_summary(violations_list, missing_items_list, state, eligibility):
    """
    Builds the core sentence fragments used in the final compliance narrative.
    """
    return {
        "state": f"This submission is filed in {state}." if state else "",
        "eligibility": (
            f"Eligibility determination: {eligibility}."
            if eligibility else ""
        ),
        "violations": (
            f"Compliance violations identified: {', '.join(violations_list)}."
            if violations_list else "No compliance violations were identified."
        ),
        "missing_items": (
            f"Missing compliance items: {', '.join(missing_items_list)}."
            if missing_items_list else "All required compliance items are present."
        ),
    }


def assemble_compliance_narrative(summary: dict) -> str:
    """
    Combines all sentence fragments into a clean, regulator-safe narrative.
    """
    parts = [
        summary.get("state", ""),
        summary.get("eligibility", ""),
        summary.get("violations", ""),
        summary.get("missing_items", "")
    ]

    return " ".join([p for p in parts if p])
