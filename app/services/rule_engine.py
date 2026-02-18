# app/services/rule_engine.py

def evaluate_rules(state_rules, customer, drivers, vehicles, coverage, guidewire):
    """
    Deterministic Rule Engine (v1)
    - Takes raw state rules
    - Normalizes them
    - Ensures each rule has a 'passed' field
    - Future versions will evaluate conditions dynamically
    """

    # 1. Extract rules from state file
    rules = (
        state_rules.get("RULES")
        or state_rules.get("rulesChecked")
        or state_rules.get("compliance", {}).get("rulesChecked")
        or []
    )

    normalized = []

    for rule in rules:
        # Ensure required fields exist
        rule_id = rule.get("ruleId") or rule.get("id") or "UNKNOWN_RULE"
        description = rule.get("description") or "No description provided"

        # v1 logic: if rule has no condition, mark as passed
        passed = rule.get("passed", True)

        normalized.append({
            "ruleId": rule_id,
            "description": description,
            "passed": passed
        })

    return normalized
