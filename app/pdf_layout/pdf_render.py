print(">>> USING REPORTLAB RENDERER <<<")

"""
Phase‑2 PDF Renderer
--------------------
This file wires the Phase‑2 context builder into the
8‑page PDF layout engine.

Responsibilities:
1. Load enriched underwriting JSON (Phase 1 output)
2. Build unified context (Phase 2)
3. Pass context into each PDF page renderer
4. Generate final multi‑page PDF

NO layout logic belongs here.
NO Phase‑3 polish belongs here.
"""

import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from app.pdf_layout.context_builder import build_context

# Import all page renderers
from app.pdf_layout.pages.executive_summary_page import render_executive_summary_page
from app.pdf_layout.pages.customer_driver_page import render_customer_driver_details_page
from app.pdf_layout.pages.vehicle_page import render_vehicle_details_page
from app.pdf_layout.pages.coverage_page import render_coverage_summary_page
from app.pdf_layout.pages.pricing_breakdown_page import render_pricing_breakdown_page
from app.pdf_layout.pages.compliance_page import render_compliance_summary_page
from app.pdf_layout.pages.ai_insights_page import render_ai_insights_summary_page
from app.pdf_layout.pages.data_lineage_page import render_data_lineage_page
from app.pdf_layout.fonts.register_fonts import register_fonts
register_fonts()

def load_phase1_output(json_path="phase2_output.json"):
    """Load enriched underwriting JSON from disk."""
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Could not load JSON file: {e}")
        return {}


def generate_pdf(output_path="test_placeholder.pdf"):
    """
    Phase‑2 PDF generation pipeline.
    1. Load enriched JSON
    2. Build context
    3. Render all 8 pages
    """

    print("Loading Phase‑1 enriched JSON...")
    enriched_json = load_phase1_output()

    print("Building Phase‑2 context...")
    context = build_context(enriched_json)

    print("Rendering PDF...")
    c = canvas.Canvas(output_path, pagesize=letter)

    # Page 1
    render_executive_summary_page(c, context, page_number=1)

    # Page 2
    render_customer_driver_details_page(c, context, page_number=2)

    # Page 3
    render_vehicle_details_page(c, context, page_number=3)

    # Page 4
    render_coverage_summary_page(c, context, page_number=4)

    # Page 5
    render_pricing_breakdown_page(c, context, page_number=5)

    # Page 6
    render_compliance_summary_page(c, context, page_number=6)

    # Page 7
    render_ai_insights_summary_page(c, context, page_number=7)

    # Page 8
    render_data_lineage_page(c, context, page_number=8)

    c.save()
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    generate_pdf()
