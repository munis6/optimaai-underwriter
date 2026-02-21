# coverage_narrative.py

from ai_narratives.tone_controller import apply_tone_control

def generate_coverage_narrative(data: dict) -> str:
    """
    Generates a clean, regulator-safe coverage narrative
    based on normalized JSON fields.
    """
    inputs = extract_coverage_inputs(data)

    coverage_list = summarize_coverages(inputs["coverages"])
    exclusions_list = summarize_exclusions(inputs["exclusions"])

    summary = build_coverage_summary(
        coverage_list,
        exclusions_list,
        inputs["full_coverage_indicator"]
    )

    return apply_tone_control(assemble_coverage_narrative(summary))

def extract_coverage_inputs(data: dict) -> dict:
    """
    Extracts all fields needed for the coverage narrative.
    """
    return {
        "coverages": data.get("coverages", {}),
        "exclusions": data.get("exclusions", {}),
        "full_coverage_indicator": data.get("fullCoverageIndicator"),
    }


def summarize_coverages(coverages: dict) -> list:
    """
    Converts coverage fields into short human-readable phrases.
    """
    results = []
    for key, value in coverages.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def summarize_exclusions(exclusions: dict) -> list:
    """
    Converts exclusion fields into short human-readable phrases.
    """
    results = []
    for key, value in exclusions.items():
        if value:
            results.append(key.replace("_", " ").title())
    return results


def build_coverage_summary(coverage_list, exclusions_list, full_indicator):
    """
    Builds the core sentence fragments used in the final coverage narrative.
    """
    return {
        "indicator": (
            f"Full coverage indicator: {full_indicator}."
            if full_indicator else ""
        ),
        "coverages": (
            f"Coverages included: {', '.join(coverage_list)}."
            if coverage_list else "No coverages were listed."
        ),
        "exclusions": (
            f"Exclusions applied: {', '.join(exclusions_list)}."
            if exclusions_list else "No exclusions were applied."
        ),
    }


def assemble_coverage_narrative(summary: dict) -> str:
    """
    Combines all sentence fragments into a clean, regulator-safe narrative.
    """
    parts = [
        summary.get("indicator", ""),
        summary.get("coverages", ""),
        summary.get("exclusions", "")
    ]

    return " ".join([p for p in parts if p])
