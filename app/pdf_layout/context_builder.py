from app.normalizer.normalizer import normalize_incoming_json

"""
Phase‑2 Context Builder
-----------------------
Takes the enriched underwriting JSON (Phase 1 output)
and converts it into a clean, unified context dictionary
that all PDF pages can consume.

This is the ONLY source of truth for the PDF.
"""

def build_context(enriched_json):
    """
    Phase‑2 unified context builder.
    Takes normalized JSON and exposes ALL sections to the PDF pages.
    """
    normalized = normalize_incoming_json(enriched_json)

    # Pass everything through exactly as-is
    return {
        "customer": normalized.get("customer"),
        "applicant": normalized.get("applicant"),
        "drivers": normalized.get("drivers"),
        "vehicles": normalized.get("vehicles"),
        "coverage": normalized.get("coverage"),
        "policy": normalized.get("policy"),
        "pricing": normalized.get("pricing"),
        "risk": normalized.get("risk"),
        "summary": normalized.get("summary"),
        "compliance": normalized.get("compliance"),
        "aiInsights": normalized.get("aiInsights"),
        "lineage": normalized.get("lineage"),
    }
