# Iowa Auto Insurance Compliance Rules
# Source: Iowa regulatory bulletin (Effective July 1, 2020)

RULES = [
    {
        "ruleId": "IA-PROHIBITED-01",
        "description": "Credit information, including credit score, cannot be used to determine premiums.",
        "logicHint": {
            "type": "FIELD_NOT_PRESENT",
            "checkType": "FIELD_NOT_PRESENT_IN_RATING"
        },
        "category": "",          # PROHIBITED_FACTOR | RATING_RULE | FAIRNESS_RULE | DOCUMENTATION_RULE
        "severity": "",          # HIGH | MEDIUM | LOW
        "impact": "",            # REQUIRES_UNDERWRITER_REVIEW | BLOCK_POLICY_ISSUANCE | NO_ACTION_REQUIRED | REQUIRES_DOCUMENTATION
        "narrative": ""          # will be filled later
    },
    {
        "ruleId": "IA-PROHIBITED-02",
        "description": "Marital status cannot be used to determine premiums.",
        "logicHint": {
            "type": "FIELD_NOT_PRESENT",
            "checkType": "FIELD_NOT_PRESENT_IN_RATING"
        },
        "category": "",          # PROHIBITED_FACTOR | RATING_RULE | FAIRNESS_RULE | DOCUMENTATION_RULE
        "severity": "",          # HIGH | MEDIUM | LOW
        "impact": "",            # REQUIRES_UNDERWRITER_REVIEW | BLOCK_POLICY_ISSUANCE | NO_ACTION_REQUIRED | REQUIRES_DOCUMENTATION
        "narrative": ""          # will be filled later
    },
    {
        "ruleId": "IA-RATING-03",
        "description": "Premiums cannot increase for not-at-fault accidents.",
        "logicHint": {
            "type": "NO_SURCHARGE_FOR_NOT_AT_FAULT",
            "checkType": "ACCIDENT_FAULT_CHECK"
        },
        "category": "",          # PROHIBITED_FACTOR | RATING_RULE | FAIRNESS_RULE | DOCUMENTATION_RULE
        "severity": "",          # HIGH | MEDIUM | LOW
        "impact": "",            # REQUIRES_UNDERWRITER_REVIEW | BLOCK_POLICY_ISSUANCE | NO_ACTION_REQUIRED | REQUIRES_DOCUMENTATION
        "narrative": ""          # will be filled later
    },
    {
        "ruleId": "IA-FAIRNESS-04",
        "description": "Coverage cannot be declined, canceled, or nonrenewed solely because of the insured's age.",
        "logicHint": {
            "type": "ALWAYS_PASS",
            "checkType": "FAIRNESS_AUDIT"
        },
        "category": "",          # PROHIBITED_FACTOR | RATING_RULE | FAIRNESS_RULE | DOCUMENTATION_RULE
        "severity": "",          # HIGH | MEDIUM | LOW
        "impact": "",            # REQUIRES_UNDERWRITER_REVIEW | BLOCK_POLICY_ISSUANCE | NO_ACTION_REQUIRED | REQUIRES_DOCUMENTATION
        "narrative": ""          # will be filled later
    },
    {
        "ruleId": "IA-RATING-05",
        "description": "Insurer cannot impose a surcharged rate solely because of the insured's age.",
        "logicHint": {
            "type": "ALWAYS_PASS",
            "checkType": "FAIRNESS_AUDIT"
        }
    },
    {
        "ruleId": "IA-FAIRNESS-06",
        "description": "Coverage cannot be declined, canceled, or nonrenewed solely because the insured is a member of the military.",
        "logicHint": {
            "type": "ALWAYS_PASS",
            "checkType": "FAIRNESS_AUDIT"
        },
        "category": "",          # PROHIBITED_FACTOR | RATING_RULE | FAIRNESS_RULE | DOCUMENTATION_RULE
        "severity": "",          # HIGH | MEDIUM | LOW
        "impact": "",            # REQUIRES_UNDERWRITER_REVIEW | BLOCK_POLICY_ISSUANCE | NO_ACTION_REQUIRED | REQUIRES_DOCUMENTATION
        "narrative": ""          # will be filled later
    },
    {
        "ruleId": "IA-FAIRNESS-07",
        "description": "Coverage cannot be denied because military members live in shared or temporary housing.",
        "logicHint": {
            "type": "ALWAYS_PASS",
            "checkType": "FAIRNESS_AUDIT"
        },
        "category": "",          # PROHIBITED_FACTOR | RATING_RULE | FAIRNESS_RULE | DOCUMENTATION_RULE
        "severity": "",          # HIGH | MEDIUM | LOW
        "impact": "",            # REQUIRES_UNDERWRITER_REVIEW | BLOCK_POLICY_ISSUANCE | NO_ACTION_REQUIRED | REQUIRES_DOCUMENTATION
        "narrative": ""          # will be filled later
    }
]
