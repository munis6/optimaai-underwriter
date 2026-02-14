from fastapi import APIRouter, Response
from pydantic import BaseModel

print(">>> ROUTER.PY LOADED <<<")

# Existing imports
from app.processor.processor import process_data
from app.dispatcher.dispatcher import dispatch_output

# Phase 4 imports
from app.services.pdf_generator import generate_compliance_pdf

# Models
from app.models.compliance_summary import ComplianceSummary

router = APIRouter()

@router.get("/")
def home():
    return {"message": "OptimaAI Underwriter is running"}

class UnderwriterInput(BaseModel):
    data: dict

@router.post("/receive")
def receive_input(payload: UnderwriterInput):
    processed = process_data(payload.data)
    final_output = dispatch_output(processed)
    return final_output

@router.post("/generate-compliance-report")
def generate_compliance_report(payload: dict):

    # Extract processed_data block
    processed = payload.get("processed_data", {})

    # Extract the three sections we need
    state_compliance = processed.get("stateCompliance", {})
    underwriting = processed.get("underwriting", {})
    ai_insights = processed.get("aiInsights", {})

    # ---------------------------------------------------------
    # Build the Pydantic ComplianceSummary object
    # ---------------------------------------------------------
    summary_obj = ComplianceSummary(
        state=state_compliance.get("state"),
        stateFullName=state_compliance.get("stateFullName"),
        overallComplianceStatus=state_compliance.get("overallComplianceStatus"),
        rulesChecked=state_compliance.get("rulesChecked", []),
        complianceSummary=state_compliance.get("notes", ""),
        underwritingSummary=underwriting,
        aiInsightsSummary=ai_insights
    )

    summary_dict = summary_obj.model_dump()

    print("\n\n===== SUMMARY DICT =====")
    for k, v in summary_dict.items():
        print(k, "=>", v)
    print("========================\n\n")

    # ---------------------------------------------------------
    # Generate PDF
    # ---------------------------------------------------------
    pdf_bytes = generate_compliance_pdf(summary_dict)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=compliance_report.pdf"
        }
    )

