# app/processor/state_compliance_builder.py

from app.compliance.state_loader import load_state_rules
from app.compliance.compliance_engine import evaluate_rules
from app.compliance.state_normalizer import normalize_state, STATE_NAME

def build_state_compliance(extracted):
    """
    Build the state-aware compliance block.
    This function is called from decision_builder.py.
    """

    # 1. Extract state from multiple possible locations
    state_raw = (
        extracted.get("state")
        or extracted.get("guidewire", {}).get("state")
        or extracted.get("customer", {}).get("address", {}).get("state")
        or extracted.get("policy", {}).get("riskState")
        or None
    )

    # 2. Normalize state (e.g., "California" → "CA")
    state_code = normalize_state(state_raw)
    if not state_code:
        state_code = "UNKNOWN"

    # 3. Load rules for that state
    state_rules = load_state_rules(state_code)

    # 4. Evaluate rules
    rules_result = evaluate_rules(state_code, state_rules, extracted)

    # 5. Build final state compliance block
    return {
        "state": state_code,
        "stateFullName": STATE_NAME.get(state_code),
        "rulesChecked": rules_result.get("rulesChecked", []),
        "overallComplianceStatus": rules_result.get("overallComplianceStatus", "PENDING_RULES"),
        "notes": rules_result.get("notes", "No state-specific compliance rules loaded."),
        "version": rules_result.get("version", "0.1")
    }
