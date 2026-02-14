# app/compliance/compliance_engine.py
# This file evaluates the state rules and builds the compliance block added to the enriched JSON.

def evaluate_single_rule(rule: dict, submission: dict) -> dict:
    """
    Phase 2: Evidence-enabled rule evaluation.
    Produces:
    - fieldsChecked
    - valuesObserved
    - reason
    - checkType
    """

    # ---------------------------------------------------------
    # Phase 3 Metadata Defaults + Validation
    # ---------------------------------------------------------
    category = rule.get("category", "") or "UNSPECIFIED_CATEGORY"
    severity = rule.get("severity", "") or "LOW"
    impact = rule.get("impact", "") or "NO_ACTION_REQUIRED"

    logic = rule.get("logicHint", {}) or {}
    logic_type = logic.get("type", "PLACEHOLDER")
    check_type = logic.get("checkType")

    fields_checked = []
    values_observed = {}

    # ---------------------------------------------------------
    # LOGIC ROUTER — Phase 2 Evidence Mode
    # ---------------------------------------------------------

    # 1. ALWAYS_PASS
    if logic_type == "ALWAYS_PASS":
        passed = True
        reason = "Rule always passes (placeholder)."

    # 2. FIELD_NOT_PRESENT
    elif logic_type == "FIELD_NOT_PRESENT":
        field = logic.get("field")
        # Fix: ensure field is a real string
        if not field:
            field = "<missing-field-definition>"
        fields_checked = [field]
        # Fix: safely extract nested fields from submission["data"]
        values_observed[field] = submission.get(field) or submission.get("data", {}).get(field)

        if field in submission:
            passed = False
            reason = f"Field '{field}' is present but prohibited."
        else:
            passed = True
            reason = f"Field '{field}' not present."

    # 3. REQUIRES_DOCUMENT
    elif logic_type == "REQUIRES_DOCUMENT":
        doc = logic.get("document")
        fields_checked = ["documents"]
        docs = submission.get("documents", [])
        values_observed["documents"] = docs

        if doc in docs:
            passed = True
            reason = f"Document '{doc}' provided."
        else:
            passed = False
            reason = f"Document '{doc}' missing."

    # 4. REQUIRES_DOCUMENT_IF_PRIOR_INSURANCE
    elif logic_type == "REQUIRES_DOCUMENT_IF_PRIOR_INSURANCE":
        doc = logic.get("document")
        docs = submission.get("documents", [])
        had_prior = submission.get("hadPriorInsurance")

        fields_checked = ["documents", "hadPriorInsurance"]
        values_observed = {
            "documents": docs,
            "hadPriorInsurance": had_prior
        }

        if had_prior is True:
            if doc in docs:
                passed = True
                reason = f"Document '{doc}' provided."
            else:
                passed = False
                reason = f"Document '{doc}' missing."
        else:
            passed = True
            reason = "Customer reported no prior insurance; documentation not required."
            check_type = "DOCUMENT_NOT_APPLICABLE"

    # 5. NO_SURCHARGE_FOR_NOT_AT_FAULT
    elif logic_type == "NO_SURCHARGE_FOR_NOT_AT_FAULT":
        accidents = submission.get("accidents", [])
        previous_premium = submission.get("previousPremium")
        current_premium = submission.get("currentPremium")

        fields_checked = ["accidents", "previousPremium", "currentPremium"]
        values_observed = {
            "accidents": accidents,
            "previousPremium": previous_premium,
            "currentPremium": current_premium
        }

        if previous_premium is None or current_premium is None:
            passed = False
            reason = "Premium comparison not possible (missing previous or current premium)."

        else:
            has_not_at_fault = any(
                acc.get("fault") == "not-at-fault" for acc in accidents
            )

            if not has_not_at_fault:
                passed = True
                reason = "No not-at-fault accidents found."

            elif current_premium > previous_premium:
                passed = False
                reason = "Premium increased after a not-at-fault accident."

            else:
                passed = True
                reason = "Premium did not increase after not-at-fault accident."

    # 6. FALLBACK
    else:
        passed = False
        reason = "Unknown logicHint — fallback placeholder."

    # ---------------------------------------------------------
    # Phase 3 Narrative Generator
    # ---------------------------------------------------------
    if passed:
        narrative = (
            f"This rule passed. {rule.get('description', '')} "
            f"No violations were detected during evaluation."
        )
    else:
        narrative = (
            f"This rule failed. {rule.get('description', '')} "
            f"Reason: {reason}. This requires attention based on state regulations."
        )

    # ---------------------------------------------------------
    # Phase 3 Impact Escalation
    # ---------------------------------------------------------
    if not passed:
        if impact == "NO_ACTION_REQUIRED":
            impact = "REQUIRES_UNDERWRITER_REVIEW"
        elif impact == "REQUIRES_UNDERWRITER_REVIEW":
            impact = "BLOCK_POLICY_ISSUANCE"

    # ---------------------------------------------------------
    # Final rule result
    # ---------------------------------------------------------
    return {
        "ruleId": rule.get("ruleId"),
        "description": rule.get("description"),
        "passed": passed,
        "fieldsChecked": fields_checked,
        "valuesObserved": values_observed,
        "reason": reason,
        "checkType": check_type,
        "category": category,
        "severity": severity,
        "impact": impact,
        "narrative": narrative
    }



def evaluate_rules(state_code: str, state_rules: dict, submission: dict):
    """
    Phase 2: Evidence-based rule evaluation.
    Every rule must return:
    - ruleId
    - description
    - passed
    - fieldsChecked
    - valuesObserved
    - reason
    - checkType
    """
    # Case 1: State has a PENDING_RULES block (AK, AL, etc.)
    if "compliance" in state_rules:
        return state_rules["compliance"]

    # Case 2: State has real rules (FL, IA, etc.)
    rules = state_rules.get("RULES", [])

    # No rules found → PENDING_RULES
    if not rules:
        return {
            "state": state_code,
            "rulesChecked": [],
            "overallComplianceStatus": "PENDING_RULES",
            "notes": f"No state-specific compliance rules loaded for {state_code}.",
            "version": "0.1"
        }

    rules_checked = []

    # Phase 2: Evaluate each rule with evidence
    for rule in rules:
        result = evaluate_single_rule(rule, submission)
        rules_checked.append({
        "ruleId": result["ruleId"],
        "description": result["description"],
        "passed": result["passed"],
        "fieldsChecked": result.get("fieldsChecked", []),
        "valuesObserved": result.get("valuesObserved", {}),
        "reason": result.get("reason", ""),
        "checkType": result.get("checkType", ""),
        "category": result.get("category", ""),
        "severity": result.get("severity", ""),
        "impact": result.get("impact", ""),
        "narrative": result.get("narrative", "")
    })
    # --------------------------------------------------------- 
    # Phase 3 Overall Compliance Status (impact-based) 
    # --------------------------------------------------------- 
    if any(r.get("impact") == "BLOCK_POLICY_ISSUANCE" for r in rules_checked): 
        overall_status = "BLOCK_POLICY_ISSUANCE" 
    elif any(r.get("impact") == "REQUIRES_UNDERWRITER_REVIEW" for r in rules_checked): 
        overall_status = "REQUIRES_UNDERWRITER_REVIEW" 
    else: overall_status = "NO_ACTION_REQUIRED"

    # ---------------------------------------------------------
    # Phase 3 Compliance Summary Block
    # ---------------------------------------------------------
    if overall_status == "BLOCK_POLICY_ISSUANCE":
        compliance_summary = (
            f"The submission for {state_code} contains one or more violations "
            f"that require the policy to be blocked from issuance. "
            f"Review the failed rules for details."
        )
    elif overall_status == "REQUIRES_UNDERWRITER_REVIEW":
        compliance_summary = (
            f"The submission for {state_code} contains issues that require "
            f"underwriter review before the policy can be issued."
        )
    else:
        compliance_summary = (
            f"The submission for {state_code} meets all evaluated compliance "
            f"requirements. No action is required."
        )
    return {
        "state": state_code,
        "rulesChecked": rules_checked,
        "overallComplianceStatus": overall_status,
        "complianceSummary": compliance_summary,
        "notes": f"{state_code} state-specific compliance rules applied successfully.",
        "version": "1.0"
    }
