from app.compliance.compliance_engine import evaluate_rules

fake_rules = {
    "RULES": [
        {
            "ruleId": "TEST-01",
            "description": "Test rule",
            "logicHint": {"checkType": "FIELD_NOT_PRESENT_IN_RATING"}
        }
    ]
}

fake_submission = {}

result = evaluate_rules("FL", fake_rules, fake_submission)
print("RESULT:", result)
