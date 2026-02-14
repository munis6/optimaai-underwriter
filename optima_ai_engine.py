# optima_ai_engine.py

from optima_ai_processors.schema_scanner.schema_scanner_agent import SchemaScannerAgent
from optima_ai_processors.underwriting_engine.underwriting_engine_agent import UnderwritingEngineAgent
from optima_ai_processors.document_intelligence.document_intelligence_agent import DocumentIntelligenceAgent

class OptimaAIEngine:
    def __init__(self):
        self.schema_scanner = SchemaScannerAgent()
        self.underwriting_engine = UnderwritingEngineAgent()
        self.document_intelligence = DocumentIntelligenceAgent()

    def process(self, request_json: dict) -> dict:
        """
        Step 8: Pipeline Orchestrator (Upgraded)
        - Unwraps the 'data' wrapper
        - Runs Schema Scanner Agent
        - Runs Underwriting Engine Agent
        - Runs Document Intelligence Agent
        """

        if "data" not in request_json:
            return {
                "status": "error",
                "message": "Missing top-level 'data' wrapper in request."
            }

        payload = request_json["data"]

        # Step 1: Schema Scanner
        schema_result = self.schema_scanner.scan(payload)

        # Step 2: Underwriting Engine
        underwriting_result = self.underwriting_engine.evaluate(schema_result)

        # Step 3: Document Intelligence
        document_result = self.document_intelligence.analyze(payload)

        return {
            "status": "pipeline_step_3_complete",
            "schemaScan": schema_result,
            "underwriting": underwriting_result,
            "documentIntelligence": document_result
        }
