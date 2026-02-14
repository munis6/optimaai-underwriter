# optima_ai_comparison.py

class OptimaAIComparisonBuilder:
    def __init__(self):
        self.name = "OptimaAIComparisonBuilder"

    def build(self, raw_input: dict, enriched_output: dict) -> dict:
        """
        Step 13: Build the BEFORE → AFTER comparison JSON
        for demos, PDFs, and investor presentations.
        """

        return {
            "before": raw_input,
            "after": enriched_output
        }
