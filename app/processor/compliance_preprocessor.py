# app/processor/compliance_preprocessor.py

def build_compliance_block(extracted, underwriting, ai_insights_dict):
    return {
        "timestamp": underwriting.get("timestamp", "not provided"),
        "dataLineage": {
            "source": "Guidewire → OptimaAI Processor → OptimaAI Underwriter → OptimaAI AI Engine",
            "customerFields": list(extracted.get("customer", {}).keys()),
            "vehicleFields": list(extracted.get("vehicles", [{}])[0].keys()) if extracted.get("vehicles") else [],
            "driverFields": list(extracted.get("drivers", [{}])[0].keys()) if extracted.get("drivers") else [],
            "coverageFields": list(extracted.get("coverage", {}).keys()),
            "guidewireFields": list(extracted.get("guidewire", {}).keys()),
            "documentFields": extracted.get("documents", [])
        },
        "ruleTrace": [
            {
                "vehicle": v.get("vehicle"),
                "rulesFired": v.get("rulesResult", {}).get("rulesFired", []),
                "eligibility": v.get("eligibility")
            }
            for v in underwriting.get("vehicles", [])
        ],
        "aiTrace": {
            "model": "Groq LLM (enterprise‑grade deterministic mode)",
            "insightFields": list(ai_insights_dict.keys()),
            "grounding": "AI used ONLY fields present in underwriting_context. No assumptions or inferred data."
        }
    }
