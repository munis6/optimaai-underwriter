# improvement_suggestions.py

from ai_narratives.tone_controller import apply_tone_control

def generate_improvement_suggestions(data: dict) -> str:
    """
    Generates actionable, regulator-safe improvement suggestions
    based on underwriting, risk factors, and documentation completeness.
    """

    inputs = extract_improvement_inputs(data)

    suggestions = []

    # Risk factor improvements
    suggestions.extend(risk_factor_suggestions(inputs["risk_factors"]))

    # Documentation improvements
    suggestions.extend(document_suggestions(inputs["missing_documents"]))

    # Eligibility blockers
    suggestions.extend(eligibility_suggestions(inputs["eligibility_blockers"]))

    # If no suggestions found
    if not suggestions:
        suggestions.append("No improvement opportunities were identified for this submission.")

    narrative = " ".join(suggestions)
    return apply_tone_control(narrative)


def extract_improvement_inputs(data: dict) -> dict:
    """
    Extracts all fields needed for improvement suggestions.
    """
    return {
        "risk_factors": data.get("riskFactors", {}),
        "missing_documents": data.get("missingDocuments", []),
        "eligibility_blockers": data.get("eligibilityBlockers", {}),
    }


def risk_factor_suggestions(risk_factors: dict) -> list:
    """
    Maps risk factors to actionable improvement suggestions.
    """
    results = []

    mapping = {
        "high_mileage": "Reducing annual mileage may help lower the risk profile.",
        "recent_violations": "Maintaining a clean driving record over time may improve eligibility and pricing.",
        "prior_claims": "Avoiding new claims and maintaining continuous coverage may improve future pricing.",
        "young_driver": "Completing certified driver training programs may help reduce long-term risk.",
        "vehicle_high_value": "Installing approved anti-theft devices may help reduce risk for high-value vehicles.",
    }

    for key, value in risk_factors.items():
        if value and key in mapping:
            results.append(mapping[key])

    return results


def document_suggestions(missing_docs: list) -> list:
    """
    Suggests improvements based on missing documentation.
    """
    results = []

    if not missing_docs:
        return results

    for doc in missing_docs:
        results.append(f"Providing the missing document '{doc}' may help improve underwriting accuracy.")

    return results


def eligibility_suggestions(blockers: dict) -> list:
    """
    Suggests improvements based on eligibility blockers.
    """
    results = []

    mapping = {
        "lapse_in_coverage": "Maintaining continuous insurance coverage may improve eligibility.",
        "unverified_address": "Submitting proof of address may help resolve eligibility issues.",
        "unverified_driver": "Providing driver verification documents may help complete underwriting.",
        "unverified_vehicle": "Submitting vehicle documentation may help resolve eligibility blockers.",
    }

    for key, value in blockers.items():
        if value and key in mapping:
            results.append(mapping[key])

    return results
