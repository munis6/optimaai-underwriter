# ============================================================
# State Compliance Rules (Starter Template)
# ------------------------------------------------------------
# What factors each state prohibits:
#   - Things the state does NOT allow insurers to use
#     (example: credit score, ZIP code, education level, occupation)
#
# What factors each state requires:
#   - Information the state says MUST be collected
#     (example: driving history, vehicle details, garaging address)
#
# What documentation each state needs:
#   - Proof or records the insurer must keep or show
#     (example: how price was calculated, why a decision was made)
#
# What disclosures must be shown:
#   - Messages the insurer MUST tell the customer
#     (example: why their price changed, why they were denied)
#
# What fairness checks must run:
#   - Tests to ensure no illegal or biased factors were used
#     (example: no discrimination, similar customers treated the same)
# ============================================================

# ============================================================
# State rule categories (simple English explanation)
# ------------------------------------------------------------
# prohibitedFactors   -> Things the state does NOT allow insurers to use.
# requiredFactors     -> Things the state says MUST be collected.
# documentationRules  -> Proof or records the insurer MUST keep or show.
# requiredDisclosures -> Messages the insurer MUST tell the customer.
# fairnessChecks      -> Tests to ensure no illegal or biased factors were used.
# ============================================================

STATE_COMPLIANCE = {
    "MD": {
        "prohibitedFactors": [
            # e.g., "creditScore", "zipCode"
        ],
        "requiredFactors": [
            # e.g., "drivingHistory", "vehicleDetails"
        ],
        "documentationRules": [
            # e.g., "mustStorePricingBreakdown"
        ],
        "requiredDisclosures": [
            # e.g., "explainPriceChange"
        ],
        "fairnessChecks": [
            # e.g., "noProhibitedFactorsUsed"
        ]
    }
}
