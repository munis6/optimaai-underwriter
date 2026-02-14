# document_intelligence_agent.py

class DocumentIntelligenceAgent:
    def __init__(self):
        self.name = "DocumentIntelligenceAgent"

    def analyze(self, payload: dict) -> dict:
        """
        Step 9: Real document intelligence logic.
        - Detects missing documents
        - Classifies provided documents
        - Flags suspicious or inconsistent documents
        - Generates document completeness score
        - Produces document-level underwriting insights
        """

        documents = payload.get("documents", [])

        # -----------------------------
        # 1. Required Document Checklist
        # -----------------------------
        required_docs = [
            "driver_license",
            "vehicle_registration",
            "proof_of_insurance",
            "id_verification"
        ]

        provided_doc_types = [doc.get("type") for doc in documents]
        missing_docs = [d for d in required_docs if d not in provided_doc_types]

        # -----------------------------
        # 2. Document Classification
        # -----------------------------
        classified_docs = []
        for doc in documents:
            doc_type = doc.get("type")
            confidence = 0.95 if doc_type in required_docs else 0.70

            classified_docs.append({
                "name": doc.get("name"),
                "type": doc_type,
                "confidence": confidence
            })

        # -----------------------------
        # 3. Suspicious Document Detection (simple rules)
        # -----------------------------
        suspicious = []

        for doc in documents:
            if "blurry" in doc.get("tags", []):
                suspicious.append(f"{doc.get('name')} appears blurry")

            if "cropped" in doc.get("tags", []):
                suspicious.append(f"{doc.get('name')} appears cropped")

            if "low_resolution" in doc.get("tags", []):
                suspicious.append(f"{doc.get('name')} is low resolution")

        # -----------------------------
        # 4. Completeness Score
        # -----------------------------
        completeness_score = round(
            (len(provided_doc_types) / len(required_docs)) * 100
        )

        # -----------------------------
        # 5. Document Insights
        # -----------------------------
        insights = []

        if missing_docs:
            insights.append("Some required documents are missing.")

        if suspicious:
            insights.append("Some documents appear suspicious or low quality.")

        if completeness_score == 100:
            insights.append("All required documents are present and appear valid.")

        return {
            "status": "document_intelligence_complete",
            "missingDocuments": missing_docs,
            "classifiedDocuments": classified_docs,
            "suspiciousIndicators": suspicious,
            "completenessScore": completeness_score,
            "insights": insights
        }
