# services/compliance_summary_builder.py

from app.models.compliance_summary import ComplianceSummary, RuleSummary


def build_compliance_summary(state_compliance: dict,
                             underwriting: dict = None,
                             ai_insights: dict = None) -> ComplianceSummary:
    """
    Takes the raw compliance JSON and turns it into a clean,
    organized ComplianceSummary object for UI/PDF.
    """

    rules = [
        RuleSummary(
            ruleId=r["ruleId"],
            description=r["description"],
            passed=r["passed"],
            category=r.get("category", ""),
            severity=r.get("severity", ""),
            impact=r.get("impact", ""),
            narrative=r.get("narrative", ""),
            fieldsChecked=r.get("fieldsChecked", []),
            valuesObserved=r.get("valuesObserved", {}),
            reason=r.get("reason", ""),
            checkType=r.get("checkType", "")
        )
        for r in state_compliance.get("rulesChecked", [])
    ]

    summary = ComplianceSummary(
        state=state_compliance["state"],
        stateFullName=state_compliance.get("stateFullName", ""),
        overallComplianceStatus=state_compliance["overallComplianceStatus"],
        complianceSummary=state_compliance.get("complianceSummary", ""),
        rulesChecked=rules,
        version=state_compliance.get("version", "1.0"),
        underwritingSummary=underwriting,
        aiInsightsSummary=ai_insights
    )

    return summary
