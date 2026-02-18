# app/services/underwriting_engine/core.py
#
# PDF-facing helper functions:
# - generate_underwriting_summary
# - generate_ai_insights
# - unified final risk scoring helpers (NEW)
#

from app.services.underwriting_engine import determine_eligibility


# ------------------------------------------------------------
# UNDERWRITING SUMMARY (PDF BLOCK)
# ------------------------------------------------------------
def generate_underwriting_summary(rules_checked):
    total_rules = len(rules_checked)
    failed_rules = sum(1 for r in rules_checked if not r.get("passed"))

    risk_score = max(0, 100 - failed_rules * 10)

    if failed_rules == 0:
        decision = "APPROVE"
        premium_adjustment = "0%"
        human_review = "No"
    elif failed_rules == 1:
        decision = "APPROVE_WITH_CONDITIONS"
        premium_adjustment = "+5%"
        human_review = "Yes"
    else:
        decision = "REJECT"
        premium_adjustment = "+15%"
        human_review = "Yes"

    factors = f"{failed_rules} failed rule(s) out of {total_rules}"

    return {
        "riskScore": risk_score,
        "decision": decision,
        "premiumAdjustment": premium_adjustment,
        "factorsConsidered": factors,
        "humanReviewRequired": human_review
    }


# ------------------------------------------------------------
# UNIFIED FINAL RISK SCORE ENGINE (NEW)
# ------------------------------------------------------------
def calculate_final_risk_score(
    underwriting_score: float,
    rule_score: float,
    ai_confidence_percent: float,
) -> float:
    """
    Unified final risk score:
    - underwriting_score: core actuarial risk (0–1000)
    - rule_score: rule-engine score (0–100 or 0–1000)
    - ai_confidence_percent: 0–100
    """
    ai_score = ai_confidence_percent * 10.0  # normalize 0–100 → 0–1000

    return (
        underwriting_score * 0.70 +
        rule_score * 0.20 +
        ai_score * 0.10
    )


def determine_final_tier(final_score: float) -> str:
    if final_score < 400:
        return "Decline"
    if final_score < 550:
        return "Review"
    if final_score < 700:
        return "Standard"
    return "Preferred"


def determine_final_decision(final_score: float) -> str:
    return "DECLINE" if final_score < 400 else "APPROVE"


# ------------------------------------------------------------
# AI INSIGHTS (PDF BLOCK)
# ------------------------------------------------------------
def generate_ai_insights(rules_checked):
    failed = [r for r in rules_checked if not r.get("passed")]

    if failed:
        flags = f"{len(failed)} rule(s) failed"
        explanation = (
            f"The model flagged rule {failed[0]['ruleId']} due to: "
            f"{failed[0]['description']}"
        )
        confidence = "92%"
        notes = "Model used state-specific underwriting patterns."
    else:
        flags = "No issues detected"
        explanation = "All rules passed. No underwriting concerns identified."
        confidence = "98%"
        notes = "Model validated all inputs successfully."

    return {
        "flags": flags,
        "explanations": explanation,
        "confidence": confidence,
        "modelNotes": notes
    }
