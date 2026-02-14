# optima_ai_formatter.py

class OptimaAIFormatter:
    def __init__(self):
        self.name = "OptimaAIFormatter"

    def format(self, pipeline_output: dict) -> dict:
        """
        Step 11: Convert raw pipeline output into a clean,
        demo-ready enriched JSON for PDF generation and demos.
        """

        schema = pipeline_output.get("schemaScan", {})
        underwriting = pipeline_output.get("underwriting", {})
        documents = pipeline_output.get("documentIntelligence", {})

        enriched = {
            "submissionId": schema.get("normalized", {}).get("submissionId"),
            "state": schema.get("normalized", {}).get("state"),
            "driversCount": schema.get("normalized", {}).get("driversCount"),
            "vehiclesCount": schema.get("normalized", {}).get("vehiclesCount"),

            "riskScore": underwriting.get("riskScore"),
            "riskLevel": underwriting.get("riskLevel"),
            "eligibility": underwriting.get("eligibility"),
            "aiEstimatedPremium": underwriting.get("aiEstimatedPremium"),
            "underwriterNotes": underwriting.get("underwriterNotes", []),

            "missingDocuments": documents.get("missingDocuments", []),
            "documentCompletenessScore": documents.get("completenessScore"),
            "documentInsights": documents.get("insights", []),

            "pipelineStatus": pipeline_output.get("status")
        }

        return enriched
