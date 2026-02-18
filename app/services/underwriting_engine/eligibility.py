def determine_eligibility(risk_score, rules_checked):
    """
    Centralized eligibility logic (v1).
    Future versions will use:
    - rule failures
    - risk thresholds
    - state-specific restrictions
    """

    # v1 logic: always eligible unless a rule explicitly fails
    for rule in rules_checked:
        if rule.get("passed") is False:
            return "Review Required"

    return "Eligible"