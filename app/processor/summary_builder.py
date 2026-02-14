def build_summary(underwriting):
    vehicles = underwriting.get("vehicles", [])
    vehicle_count = len(vehicles)
    total_premium = sum(v.get("premium", 0) for v in vehicles)

    eligibilities = [v.get("eligibility") for v in vehicles]

    if "Decline" in eligibilities:
        overall_eligibility = "Decline"
    elif "Review" in eligibilities:
        overall_eligibility = "Review"
    else:
        overall_eligibility = "Eligible"

    highest_risk_vehicle = None
    if vehicles:
        highest_risk_vehicle = max(vehicles, key=lambda v: v.get("riskScore", 0))
        highest_risk_vehicle = highest_risk_vehicle.get("vehicle")

    return {
        "vehicleCount": vehicle_count,
        "totalPremium": total_premium,
        "overallEligibility": overall_eligibility,
        "highestRiskVehicle": highest_risk_vehicle
    }
