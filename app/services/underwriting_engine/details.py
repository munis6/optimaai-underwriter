def build_underwriting_details(drivers, vehicles, risk_score, base_premium):
    """
    Centralized underwriting detail builder.
    Produces underwriting.vehicles and underwriting.drivers blocks.
    """

    eligibility = "Eligible"

    uw_vehicles = [
        {
            "vehicle": v["raw"],
            "rulesResult": {"rulesFired": [], "status": "rules evaluated (placeholder)"},
            "riskScore": risk_score,
            "premium": base_premium,
            "eligibility": eligibility,
        }
        for v in vehicles
    ]

    uw_drivers = [
        {
            "firstName": d["raw"].get("firstName"),
            "lastName": d["raw"].get("lastName"),
            "age": d["raw"].get("age"),
            "licenseNumber": d["raw"].get("licenseNumber"),
            "yearsLicensed": d["raw"].get("yearsLicensed"),
            "accidents": d["raw"].get("accidents"),
            "violations": d["raw"].get("violations"),
            "claims": d["raw"].get("claims"),
            "isPrimaryDriver": d["raw"].get("isPrimaryDriver"),
        }
        for d in drivers
    ]

    return {
        "vehicles": uw_vehicles,
        "drivers": uw_drivers,
        "eligibility": eligibility
    }