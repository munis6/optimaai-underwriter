def parse_ai_output(ai_output):
    try:
        driver, pricing, explanation, improvement = [
            x.strip() for x in ai_output.split("||")
        ]
    except Exception:
        driver = pricing = explanation = improvement = ai_output

    return {
        "driverRiskFactors": driver,
        "pricingRationale": pricing,
        "explanations": explanation,
        "improvementSuggestions": improvement
    }
