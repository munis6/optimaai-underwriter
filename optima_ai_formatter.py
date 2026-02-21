from ai_narratives.pricing_narrative import generate_pricing_narrative
from ai_narratives.coverage_narrative import generate_coverage_narrative
from ai_narratives.compliance_narrative import generate_compliance_narrative
from ai_narratives.eligibility_narrative import generate_eligibility_narrative
from ai_narratives.improvement_suggestions import generate_improvement_suggestions
from ai_narratives.driver_narrative import generate_driver_narratives
from ai_narratives.vehicle_narrative import generate_vehicle_narratives


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

            # ⭐ NEW: AI Narratives integrated
            "pricingNarrative": generate_pricing_narrative(underwriting),
            "coverageNarrative": generate_coverage_narrative(schema.get("normalized", {})),
            "complianceNarrative": generate_compliance_narrative(schema.get("normalized", {})),
            "eligibilityNarrative": generate_eligibility_narrative(underwriting),

            # ⭐ NEW: Improvement Suggestions 
            "improvementSuggestions": generate_improvement_suggestions({ 
            "riskFactors": underwriting.get("riskFactors", {}), 
            "missingDocuments": documents.get("missingDocuments", []), 
            "eligibilityBlockers": underwriting.get("eligibilityBlockers", {}) }),

            # ⭐ NEW: Driver-Level Narratives 
            "driverNarratives": generate_driver_narratives( 
                schema.get("normalized", {}).get("drivers", []) 
            ),

            "vehicleNarratives": generate_vehicle_narratives(
                schema.get("normalized", {}).get("vehicles", [])
            ),

            "pipelineStatus": pipeline_output.get("status")
        }

        return enriched
