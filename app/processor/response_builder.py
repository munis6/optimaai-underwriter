# app/processor/response_builder.py

from app.services.underwriting_engine import (
    generate_underwriting_summary,
    generate_ai_insights
)

def build_final_response(
    state,
    state_full_name,
    overall_status,
    compliance_summary,
    rules_checked,
    transaction_id,
    timestamp
):
    """
    Assembles the final JSON response that the PDF generator expects.
    """

    # Underwriting + AI insights
    underwriting_summary = generate_underwriting_summary(rules_checked)
    ai_insights_summary = generate_ai_insights(rules_checked)

    # Final JSON structure
    summary = {
        "transactionId": transaction_id,
        "timestamp": timestamp,
        "state": state,
        "stateFullName": state_full_name,
        "overallComplianceStatus": overall_status,
        "complianceSummary": compliance_summary,
        "rulesChecked": rules_checked,
        "underwritingSummary": underwriting_summary,
        "aiInsightsSummary": ai_insights_summary
    }

    return summary
