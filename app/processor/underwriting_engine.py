# underwriting_engine.py

def apply_rules(customer, vehicle, coverage):
    rules_fired = []

    if customer.get("age", 0) < 18:
        rules_fired.append("RULE:MINIMUM_AGE_FAILED")

    if vehicle.get("year", 0) < 2000:
        rules_fired.append("RULE:OLD_VEHICLE_SURCHARGE")

    if coverage.get("deductible", 0) < 500:
        rules_fired.append("RULE:LOW_DEDUCTIBLE_SURCHARGE")

    return {
        "rulesFired": rules_fired,
        "status": "rules evaluated (placeholder)"
    }

def calculate_risk_score(customer, vehicle):
    base = 600

    if customer.get("age", 0) < 25:
        base -= 50

    if vehicle.get("year", 0) < 2010:
        base -= 30

    return max(300, min(850, base))


def calculate_premium(coverage, risk_score):
    base = 500
    base += (850 - risk_score) * 0.5

    if coverage.get("deductible", 0) < 500:
        base += 100

    return round(base, 2)


def determine_eligibility(risk_score):
    if risk_score < 400:
        return "Decline"
    if risk_score < 600:
        return "Review"
    return "Eligible"

def run_underwriting(customer, vehicles, coverage, drivers):
    vehicle_underwriting = []

    for v in vehicles:
        rules_result = apply_rules(customer, v, coverage)
        risk_score = calculate_risk_score(customer, v)
        premium = calculate_premium(coverage, risk_score)
        eligibility = determine_eligibility(risk_score)

        vehicle_underwriting.append({
            "vehicle": v,
            "rulesResult": rules_result,
            "riskScore": risk_score,
            "premium": premium,
            "eligibility": eligibility
        })

    underwriting = {
        "customer": customer,
        "coverage": coverage,
        "vehicles": vehicle_underwriting,
        "drivers": drivers
    }

    return underwriting
