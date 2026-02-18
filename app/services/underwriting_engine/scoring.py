def calculate_risk_score(customer, drivers, vehicles, coverage, guidewire):
    print(">>> REAL SCORING ENGINE EXECUTED")

    """
    Deterministic OptimaAI Risk Score Model (v1)
    Range: 300–900
    Base Score: 700
    """

    score = 700

    # 1. Age
    age = customer.get("age")
    if age:
        if 25 <= age <= 70: score += 0
        elif 21 <= age <= 24: score -= 40
        elif 18 <= age <= 20: score -= 80
        elif 71 <= age <= 75: score -= 30
        elif age >= 76: score -= 60

    # 2. Accidents
    accidents = drivers[0]["raw"].get("accidents", 0) if drivers else 0
    if accidents == 1: score -= 80
    elif accidents == 2: score -= 140
    elif accidents >= 3: score -= 200

    # 3. Violations
    violations = drivers[0]["raw"].get("violations", 0) if drivers else 0
    major = drivers[0]["raw"].get("majorViolation", False) if drivers else False
    if major:
        score -= 220
    else:
        if violations == 1: score -= 40
        elif violations == 2: score -= 80
        elif violations >= 3: score -= 120

    # 4. Mileage
    mileage = vehicles[0]["raw"].get("annualMileage") if vehicles else None
    if mileage:
        if mileage <= 7500: score += 20
        elif mileage <= 15000: score += 0
        elif mileage <= 20000: score -= 30
        else: score -= 60

    # 5. Vehicle type
    if vehicles:
        v = vehicles[0]["raw"]
        model = (v.get("model") or "").lower()
        year = v.get("year")

        safe = ["civic", "corolla", "camry", "accord"]
        family = ["odyssey", "sienna", "highlander", "pilot", "rav4", "cr-v"]
        sports = ["mustang", "camaro", "challenger", "corvette", "charger"]

        if any(s in model for s in safe): score += 20
        if any(f in model for f in family): score += 10
        if any(s in model for s in sports): score -= 80

        if year and (2025 - int(year) > 15): score -= 30

    # 6. Coverage
    ctype = coverage.get("coverageType", "").lower()
    liability = coverage.get("liabilityLimit", 100000)
    deductible = coverage.get("deductible", 500)

    if ctype == "liability": score += 10
    else: score -= 20

    if liability > 250000: score -= 20
    if deductible < 500: score -= 20

    # 7. ZIP
    zip_code = (customer.get("raw") or {}).get("address", {}).get("zip")
    if zip_code:
        z = str(zip_code)
        if z.startswith(("50", "51", "52")): score += 20
        elif z.startswith(("60", "61", "62")): score += 0
        else: score -= 40

    # 8. State
    state = guidewire.get("state")
    high = ["FL", "LA", "MI", "NY"]
    low = ["IA", "ND", "SD", "VT"]

    if state in high: score -= 20
    elif state in low: score += 10

    return max(300, min(900, score))
