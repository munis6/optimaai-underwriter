def build_executive_summary(summary: dict) -> str:
    highest = summary.get("highestRiskVehicle") or {}
    year = highest.get("year", "N/A")
    make = highest.get("make", "N/A")
    model = highest.get("model", "N/A")

    return (
        f"The highest-risk vehicle is the {year} {make} {model}. "
        f"Overall underwriting risk level: {summary.get('overallRiskLevel', 'Unknown')}."
    )
