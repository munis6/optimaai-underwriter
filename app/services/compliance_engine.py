# app/services/compliance_engine.py

def build_compliance_block(
    state,
    compliance_meta,
    rules_checked,
    customer_raw,
    vehicles_raw,
    drivers_raw,
    coverage_raw,
    guidewire_raw
):
    """
    Centralized Compliance + Lineage Builder (v1)
    Produces:
    - stateCompliance
    - compliance (lineage + ruleTrace + aiTrace)
    """

    # -----------------------------
    # State Compliance Block
    # -----------------------------
    state_compliance = {
        "state": compliance_meta.get("state", state),
        "stateFullName": compliance_meta.get("stateFullName", "Unknown"),
        "rulesChecked": rules_checked,
        "overallComplianceStatus": compliance_meta.get("overallComplianceStatus", "PENDING_RULES"),
        "notes": compliance_meta.get("notes", f"No state-specific compliance rules loaded for {state}."),
        "version": compliance_meta.get("version", "1.0"),
    }

    # -----------------------------
    # Compliance Lineage Block
    # -----------------------------
    compliance = {
        "timestamp": "not provided",
        "dataLineage": {
            "source": "Guidewire → OptimaAI → Underwriter → AI Engine",
            "customerFields": list(customer_raw.keys()),
            "vehicleFields": list((vehicles_raw[0] or {}).keys()) if vehicles_raw else [],
            "driverFields": list((drivers_raw[0] or {}).keys()) if drivers_raw else [],
            "coverageFields": list(coverage_raw.keys()),
            "guidewireFields": list(guidewire_raw.keys()),
            "documentFields": [],
        },
        "ruleTrace": rules_checked,
        "aiTrace": {
            "model": "Groq LLM (deterministic)",
            "insightFields": ["flags", "explanations", "confidence", "modelNotes"],
            "grounding": "AI used only provided underwriting context.",
        },
    }

    return state_compliance, compliance
