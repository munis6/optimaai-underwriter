def build_ai_insights(customer, coverage, risk_score):
    """
    Builds the non-summary AI insights block.
    """

    driver_name = f"{customer.get('firstName')} {customer.get('lastName')}".strip()

    ai_insights = {
        "driverRiskFactors": f"Driver {driver_name} has a moderate risk score of {risk_score}.",
        "pricingRationale": (
            f"Pricing is based on liability ${coverage['liabilityLimit']:,}, "
            f"deductible ${coverage['deductible']:,}, "
            f"coverage {coverage['coverageType']}."
        ),
        "explanations": "Driver has a clean record with no accidents or violations.",
        "improvementSuggestions": "Consider telematics, defensive driving, and safety features.",
    }

    return ai_insights