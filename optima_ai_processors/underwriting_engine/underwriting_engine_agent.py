# underwriting_engine_agent.py

class UnderwritingEngineAgent:
    def __init__(self):
        self.name = "UnderwritingEngineAgent"

    def evaluate(self, schema_output: dict) -> dict:
        """
        Step 7: Real underwriting logic.
        Uses normalized data from Schema Scanner to generate:
        - risk score
        - risk level
        - eligibility
        - missing info detection
        - underwriting notes
        - simple premium estimation
        """

        normalized = schema_output.get("normalized", {})

        # -----------------------------
        # 1. Basic Risk Score Calculation
        # -----------------------------
        base_score = 600

        # Age factor
        # (Younger drivers = higher risk)
        age = None
        if "driversCount" in normalized and normalized["driversCount"] > 0:
            # We don't have age here, so we infer from schema_output
            # (This is placeholder logic — later we will pass full driver data)
            age = 34  # placeholder for demo
            if age < 25:
                base_score -= 80
            elif age < 30:
                base_score -= 40
            else:
                base_score += 20

        # Accident factor
        if normalized.get("hasAccidents"):
            base_score -= 120

        # Violations factor
        if normalized.get("hasViolations"):
            base_score -= 100

        # State factor (placeholder)
        state = normalized.get("state")
        if state == "CA":
            base_score -= 40
        elif state == "IA":
            base_score += 10

        # Clamp score
        risk_score = max(300, min(850, base_score))

        # -----------------------------
        # 2. Risk Level
        # -----------------------------
        if risk_score >= 700:
            risk_level = "Low"
        elif risk_score >= 550:
            risk_level = "Medium"
        else:
            risk_level = "High"

        # -----------------------------
        # 3. Eligibility
        # -----------------------------
        eligibility = "Eligible" if risk_level != "High" else "Review Required"

        # -----------------------------
        # 4. Missing Information
        # -----------------------------
        missing_info = []

        if "submissionId" not in schema_output.get("receivedKeys", []):
            missing_info.append("submissionId")

        if not normalized.get("state"):
            missing_info.append("state")

        # -----------------------------
        # 5. Underwriter Notes
        # -----------------------------
        notes = []

        if risk_level == "Low":
            notes.append("Applicant presents a stable and low-risk profile.")
        elif risk_level == "Medium":
            notes.append("Applicant is generally acceptable but requires standard review.")
        else:
            notes.append("High-risk indicators detected. Manual underwriting recommended.")

        if normalized.get("hasAccidents"):
            notes.append("Accident history detected — verify loss runs.")

        if normalized.get("hasViolations"):
            notes.append("Violation history detected — confirm MVR details.")

        # -----------------------------
        # 6. Simple Premium Estimation
        # -----------------------------
        # Placeholder model: lower risk score = higher premium
        ai_estimated_premium = round(2000 - (risk_score * 1.2))

        return {
            "status": "underwriting_complete",
            "riskScore": risk_score,
            "riskLevel": risk_level,
            "eligibility": eligibility,
            "missingInformation": missing_info,
            "underwriterNotes": notes,
            "aiEstimatedPremium": ai_estimated_premium,
            "normalizedUsed": normalized
        }
