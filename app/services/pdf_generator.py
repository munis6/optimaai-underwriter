import os
import pdfkit
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ---------------------------------------------------------
# TEMPLATE LOADER
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"])
)

template = env.get_template("compliance_summary_template.html")

# ---------------------------------------------------------
# PDF GENERATOR
# ---------------------------------------------------------
config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")

def generate_compliance_pdf(summary: dict) -> bytes:
    rendered_html = template.render(
        state=summary.get("state"),
        stateFullName=summary.get("stateFullName"),
        overallComplianceStatus=summary.get("overallComplianceStatus"),
        complianceSummary=summary.get("complianceSummary"),
        rulesChecked=summary.get("rulesChecked", []),
        underwritingSummary=summary.get("underwritingSummary", {}),
        aiInsightsSummary=summary.get("aiInsightsSummary", {}),
    )

    options = {
        "enable-local-file-access": None
    }

    pdf_bytes = pdfkit.from_string(
        rendered_html,
        False,
        configuration=config,
        options=options
    )

    return pdf_bytes


# ---------------------------------------------------------
# STEP 12: OPTIMAAI ENRICHED JSON → PDF ADAPTER
# ---------------------------------------------------------
def generate_optimaai_pdf(enriched: dict) -> bytes:
    """
    Step 12: Convert enriched OptimaAI JSON into the summary dict
    expected by the existing Jinja2 PDF generator.
    """

    summary = {
        "state": enriched.get("state"),
        "stateFullName": enriched.get("state"),  # placeholder until mapping added
        "overallComplianceStatus": enriched.get("eligibility"),

        "complianceSummary": {
            "riskScore": enriched.get("riskScore"),
            "riskLevel": enriched.get("riskLevel"),
            "aiEstimatedPremium": enriched.get("aiEstimatedPremium"),
        },

        "rulesChecked": [],  # optional for now

        "underwritingSummary": {
            "notes": enriched.get("underwriterNotes", []),
        },

        "aiInsightsSummary": {
            "missingDocuments": enriched.get("missingDocuments", []),
            "documentCompletenessScore": enriched.get("documentCompletenessScore"),
            "documentInsights": enriched.get("documentInsights", []),
        }
    }

    return generate_compliance_pdf(summary)
