from fastapi import APIRouter, Response
from pydantic import BaseModel

from app.processor.processor import process_data
from app.dispatcher.dispatcher import dispatch_output
from app.pdf_layout.pdf_render import generate_pdf
from app.models.compliance_summary import ComplianceSummary

router = APIRouter()

class UnderwriterInput(BaseModel):
    data: dict

@router.get("/")
def home():
    return {"message": "OptimaAI Underwriter is running"}

@router.post("/receive")
def receive_input(payload: UnderwriterInput):
    processed = process_data(payload.data)
    final_output = dispatch_output(processed)

    risk_score = final_output.get("finalDecision", {}).get("riskScore")

    return {
        "status": "received",
        "riskScore": risk_score
    }

@router.post("/generate-compliance-report")
def generate_compliance_report(payload: dict):
    processed = payload.get("processed_data", {})

    summary_obj = ComplianceSummary(
        state=None,
        stateFullName=None,
        overallComplianceStatus=None,
        rulesChecked=[],
        complianceSummary="",
        underwritingSummary={},
        aiInsightsSummary={},
    )

    output_path = "test_placeholder.pdf"
    generate_pdf(output_path)

    with open(output_path, "rb") as f:
        pdf_bytes = f.read()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=compliance_report.pdf"},
    )
