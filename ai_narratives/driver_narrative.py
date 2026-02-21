# driver_narrative.py

from ai_narratives.tone_controller import apply_tone_control

def generate_driver_narratives(drivers: list) -> list:
    """
    Generates a list of per-driver narratives.
    Each driver receives a clean, regulator-safe explanation
    of their individual risk profile.
    """

    if not drivers:
        return []

    narratives = []

    for driver in drivers:
        summary = build_driver_summary(driver)
        narrative = assemble_driver_narrative(summary)
        narratives.append(apply_tone_control(narrative))

    return narratives


def build_driver_summary(driver: dict) -> dict:
    """
    Extracts and formats driver-level risk signals.
    """

    return {
        "name": driver.get("name", "This driver"),
        "age": driver.get("age"),
        "experience": driver.get("yearsLicensed"),
        "violations": driver.get("violations", []),
        "claims": driver.get("claims", []),
        "mileage": driver.get("annualMileage"),
        "risk_flags": driver.get("riskFlags", {}),
    }


def assemble_driver_narrative(summary: dict) -> str:
    """
    Converts driver attributes into a clean narrative.
    """

    parts = []

    # Name
    parts.append(f"{summary['name']} has been evaluated based on age, driving history, and annual usage.")

    # Age
    if summary["age"] is not None:
        if summary["age"] < 25:
            parts.append("Younger age contributes to a higher risk profile.")
        elif summary["age"] > 70:
            parts.append("Senior driver age may contribute to a slightly elevated risk profile.")
        else:
            parts.append("Driver age falls within a standard risk range.")

    # Experience
    if summary["experience"] is not None:
        if summary["experience"] < 3:
            parts.append("Limited driving experience increases overall risk.")
        else:
            parts.append("Driving experience is consistent with stable risk.")

    # Violations
    if summary["violations"]:
        parts.append(f"Recent violations include: {', '.join(summary['violations'])}.")
    else:
        parts.append("No recent violations were reported.")

    # Claims
    if summary["claims"]:
        parts.append(f"Prior claims include: {', '.join(summary['claims'])}.")
    else:
        parts.append("No prior claims were reported.")

    # Mileage
    if summary["mileage"] is not None:
        if summary["mileage"] > 15000:
            parts.append("Higher annual mileage contributes to increased exposure.")
        else:
            parts.append("Annual mileage is within a typical range.")

    # Risk flags
    flagged = [k.replace('_', ' ').title() for k, v in summary["risk_flags"].items() if v]
    if flagged:
        parts.append(f"Additional risk indicators include: {', '.join(flagged)}.")
    else:
        parts.append("No additional risk indicators were identified.")

    return " ".join(parts)
