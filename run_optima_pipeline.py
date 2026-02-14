# run_optima_pipeline.py

import zipfile
import json
import os
from optima_ai_engine import OptimaAIEngine
from optima_ai_formatter import OptimaAIFormatter
from optima_ai_comparison import OptimaAIComparisonBuilder
from app.services.pdf_generator import generate_optimaai_pdf
from optima_ai_demo_bundle import OptimaAIDemoBundleBuilder


def load_test_json():
    print("RUNNER STARTED")
    with open("guidewire_request.json", "r") as f:
        return json.load(f)


if __name__ == "__main__":
    engine = OptimaAIEngine()
    formatter = OptimaAIFormatter()
    comparison_builder = OptimaAIComparisonBuilder()
    bundle_builder = OptimaAIDemoBundleBuilder()

    # Load test JSON
    request_json = load_test_json()

    # Run full OptimaAI pipeline
    result = engine.process(request_json)

    print("\n===== OPTIMAAI PIPELINE OUTPUT =====\n")
    print(json.dumps(result, indent=4))
    print("\n====================================\n")

    # Convert to enriched JSON
    enriched = formatter.format(result)

    print("\n===== OPTIMAAI ENRICHED JSON =====\n")
    print(json.dumps(enriched, indent=4))
    print("\n==================================\n")

    # Build BEFORE → AFTER comparison
    comparison = comparison_builder.build(request_json, enriched)

    print("\n===== BEFORE → AFTER COMPARISON =====\n")
    print(json.dumps(comparison, indent=4))
    print("\n=====================================\n")

    # Generate PDF
    pdf_bytes = generate_optimaai_pdf(enriched)

    with open("optimaai_report.pdf", "wb") as f:
        f.write(pdf_bytes)

    print("\nPDF generated: optimaai_report.pdf\n")

    # Build demo bundle
    bundle = bundle_builder.build(
        raw_input=request_json,
        pipeline_output=result,
        enriched=enriched,
        comparison=comparison,
        pdf_filename="optimaai_report.pdf"
    )

    print("\n===== OPTIMAAI DEMO BUNDLE =====\n")
    print(json.dumps(bundle, indent=4))
    print("\n================================\n")

    # ---------------------------------------------------------
    # STEP 16: SAVE ALL ASSETS INTO demo_portal/
    # ---------------------------------------------------------

    # Ensure demo portal folders exist
    os.makedirs("demo_portal/assets/json", exist_ok=True)
    os.makedirs("demo_portal/assets/pdf", exist_ok=True)

    # Save JSON assets
    with open("demo_portal/assets/json/enriched.json", "w") as f:
        json.dump(enriched, f, indent=4)

    with open("demo_portal/assets/json/pipeline_output.json", "w") as f:
        json.dump(result, f, indent=4)

    with open("demo_portal/assets/json/before_after.json", "w") as f:
        json.dump(comparison, f, indent=4)

    with open("demo_portal/assets/json/demo_bundle.json", "w") as f:
        json.dump(bundle, f, indent=4)

    # Save PDF
    with open("demo_portal/assets/pdf/optimaai_report.pdf", "wb") as f:
        f.write(pdf_bytes)

    print("\nDemo portal assets saved to demo_portal/\n")

    # ---------------------------------------------------------
# STEP 18: PACKAGE EVERYTHING INTO A DEMO ZIP BUNDLE
# ---------------------------------------------------------

zip_filename = "optimaai_demo_bundle.zip"

with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    # Add demo portal files
    zipf.write("demo_portal/index.html")
    zipf.write("demo_portal/style.css")
    zipf.write("demo_portal/app.js")

    # Add JSON assets
    zipf.write("demo_portal/assets/json/enriched.json")
    zipf.write("demo_portal/assets/json/pipeline_output.json")
    zipf.write("demo_portal/assets/json/before_after.json")
    zipf.write("demo_portal/assets/json/demo_bundle.json")

    # Add PDF
    zipf.write("demo_portal/assets/pdf/optimaai_report.pdf")

    print(f"\nDemo ZIP bundle created: {zip_filename}\n")

