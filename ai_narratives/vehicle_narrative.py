# vehicle_narrative.py

from ai_narratives.tone_controller import apply_tone_control

def generate_vehicle_narratives(vehicles: list) -> list:
    """
    Generates a list of per-vehicle narratives.
    Each vehicle receives a clean, regulator-safe explanation
    of its individual risk profile.
    """

    if not vehicles:
        return []

    narratives = []

    for vehicle in vehicles:
        summary = build_vehicle_summary(vehicle)
        narrative = assemble_vehicle_narrative(summary)
        narratives.append(apply_tone_control(narrative))

    return narratives


def build_vehicle_summary(vehicle: dict) -> dict:
    """
    Extracts and formats vehicle-level risk signals.
    """

    return {
        "year": vehicle.get("year"),
        "make": vehicle.get("make"),
        "model": vehicle.get("model"),
        "value": vehicle.get("value"),
        "usage": vehicle.get("usage"),
        "annualMileage": vehicle.get("annualMileage"),
        "safetyRating": vehicle.get("safetyRating"),
        "risk_flags": vehicle.get("riskFlags", {}),
    }


def assemble_vehicle_narrative(summary: dict) -> str:
    """
    Converts vehicle attributes into a clean narrative.
    """

    parts = []

    # Basic identification
    parts.append(
        f"The vehicle ({summary['year']} {summary['make']} {summary['model']}) "
        f"has been evaluated based on value, usage, mileage, and safety characteristics."
    )

    # Value
    if summary["value"] is not None:
        if summary["value"] > 40000:
            parts.append("Higher vehicle value may contribute to increased risk exposure.")
        else:
            parts.append("Vehicle value falls within a typical range.")

    # Usage
    if summary["usage"]:
        if summary["usage"].lower() == "commercial":
            parts.append("Commercial usage may contribute to elevated exposure.")
        else:
            parts.append("Vehicle usage is consistent with standard personal use.")

    # Mileage
    if summary["annualMileage"] is not None:
        if summary["annualMileage"] > 15000:
            parts.append("Higher annual mileage increases exposure.")
        else:
            parts.append("Annual mileage is within a typical range.")

    # Safety rating
    if summary["safetyRating"] is not None:
        if summary["safetyRating"] >= 4:
            parts.append("A strong safety rating helps reduce overall risk.")
        else:
            parts.append("A lower safety rating may contribute to increased risk.")

    # Risk flags
    flagged = [k.replace('_', ' ').title() for k, v in summary["risk_flags"].items() if v]
    if flagged:
        parts.append(f"Additional risk indicators include: {', '.join(flagged)}.")
    else:
        parts.append("No additional risk indicators were identified.")

    return " ".join(parts)
