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
#config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
config = None

def generate_compliance_pdf(summary: dict) -> bytes:
    # Extract rules safely
    rules = summary.get("rulesChecked", [])

    # FIX: Prevent PDF crash when a state has zero rules
    if not rules:
        rules = [{
            "ruleId": "N/A",
            "description": "No rules available for this state."
        }]

    rendered_html = template.render(
        state=summary.get("state"),
        stateFullName=summary.get("stateFullName"),
        overallComplianceStatus=summary.get("overallComplianceStatus"),
        complianceSummary=summary.get("complianceSummary"),
        rulesChecked=rules,   # <-- now always safe
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
    Convert enriched OptimaAI JSON into the summary dict
    expected by the existing Jinja2 PDF generator.
    """

    summary = {
        "state": enriched.get("state"),
        "stateFullName": enriched.get("stateFullName"),  # now correct
        "overallComplianceStatus": enriched.get("overallComplianceStatus"),

        "complianceSummary": {
            "riskScore": enriched.get("riskScore"),
            "riskLevel": enriched.get("riskLevel"),
            "aiEstimatedPremium": enriched.get("aiEstimatedPremium"),
        },

        "rulesChecked": enriched.get("rulesChecked", []),

        "underwritingSummary": enriched.get("underwritingSummary", {}),

        "aiInsightsSummary": enriched.get("aiInsightsSummary", {})
    }

    return generate_compliance_pdf(summary)
