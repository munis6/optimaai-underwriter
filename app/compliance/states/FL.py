# app/compliance/states/FL.py
# Florida state-specific compliance rules with logicHint metadata

RULES = [
    {
        "ruleId": "FL-PROHIBITED-01",
        "description": "Credit score cannot be used as a rating factor for private passenger auto.",
        "logicHint": {
            "type": "FIELD_NOT_PRESENT",
            "checkType": "FIELD_NOT_PRESENT_IN_RATING",
            "field": "creditScore"
        }
    },
    {
        "ruleId": "FL-REQUIRED-02",
        "description": "Hurricane deductible options must be disclosed to the insured.",
        "logicHint": {
            "type": "ALWAYS_PASS",
            "checkType": "DISCLOSURE_PRESENT"
        }
    },
    {
    "ruleId": "FL-DOCS-03",
    "description": "Proof of prior insurance must be collected before binding when prior coverage is indicated.",
    "logicHint": {
        "type": "REQUIRES_DOCUMENT_IF_PRIOR_INSURANCE",
        "document": "proofOfPriorInsurance",
        "checkType": "DOCUMENT_PRESENT"
    }
    },
    {
        "ruleId": "FL-FAIRNESS-04",
        "description": "No prohibited socio-economic factors may influence underwriting or rating decisions.",
        "logicHint": {
            "type": "ALWAYS_PASS",
            "checkType": "FAIRNESS_AUDIT"
        }
    }
]
