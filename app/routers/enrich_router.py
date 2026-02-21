from fastapi import APIRouter, Response, Body
from pydantic import BaseModel

from app.services.rule_engine import evaluate_rules
from app.services.underwriting_engine import (
    build_underwriting_details,
    build_summary_block,
    build_ai_insights,
    determine_eligibility,
)
from app.services.underwriting_engine.scoring import calculate_risk_score

from app.services.underwriting_engine.core import (
    generate_underwriting_summary,
    generate_ai_insights,
    calculate_final_risk_score,
    determine_final_tier,
    determine_final_decision,
)

from app.services.compliance_engine import build_compliance_block
print(">>> USING NEW ROUTER VERSION <<<")
print(">>> ROUTER.PY LOADED <<<")
print(">>> USING SCORING FROM:", calculate_risk_score.__module__)

from app.processor.processor import process_data
from app.dispatcher.dispatcher import dispatch_output

from app.pdf_layout.pdf_render import generate_pdf
from app.models.compliance_summary import ComplianceSummary
from app.compliance.state_loader import load_state_rules
from app.compliance.state_normalizer import STATE_NAME

router = APIRouter()


@router.get("/")
def home():
    return {"message": "OptimaAI Underwriter is running"}


@router.post("/enrich")
async def enrich(payload: dict = Body(...)):
    raw = payload or {}
    root = raw["data"]

    guidewire_raw = root.get("guidewire", {})
    state = (
        guidewire_raw.get("state")
        or root.get("state")
        or root.get("customer", {}).get("address", {}).get("state")
        or "IA"
    )

    state_rules = load_state_rules(state)
    compliance_meta = state_rules.get("compliance", {})
    rules_checked = (
        state_rules.get("RULES")
        or state_rules.get("rulesChecked")
        or compliance_meta.get("rulesChecked")
        or []
    )

    customer_raw = root.get("customer", {})
    vehicles_raw = root.get("vehicles", [])
    drivers_raw = root.get("drivers", [])
    coverage_raw = root.get("coverage", {})

    customer = {
        "firstName": customer_raw.get("firstName"),
        "lastName": customer_raw.get("lastName"),
        "age": customer_raw.get("age"),
        "licenseNumber": customer_raw.get("licenseNumber"),
        "raw": customer_raw or None,
    }

    coverage = {
        "liabilityLimit": coverage_raw.get("liabilityLimit", 100000),
        "deductible": coverage_raw.get("deductible", 500),
        "coverageType": coverage_raw.get("coverageType", "FullCoverage"),
        "raw": coverage_raw,
    }

    vehicles = [
        {
            "vin": v.get("vin"),
            "year": v.get("year"),
                       "make": v.get("make"),
            "model": v.get("model"),
            "raw": v,
        }
        for v in vehicles_raw
    ]

    drivers = [
        {
            "driverId": d.get("driverId"),
            "firstName": d.get("firstName"),
            "lastName": d.get("lastName"),
            "age": d.get("age"),
            "licenseStatus": d.get("licenseStatus"),
            "assignedVehicles": d.get("assignedVehicles", []),
            "raw": d,
        }
        for d in drivers_raw
    ]

    guidewire = {
        "transactionId": guidewire_raw.get("transactionId"),
        "timestamp": guidewire_raw.get("timestamp"),
        "sourceSystem": guidewire_raw.get("sourceSystem"),
        "state": guidewire_raw.get("state"),
        "raw": guidewire_raw,
    }

    base_premium = 625.0

    # -----------------------------
    # Actuarial Risk Score
    # -----------------------------
    risk_score = calculate_risk_score(
        customer,
        drivers,
        vehicles,
        coverage,
        guidewire,
    )

    underwriting_summary = generate_underwriting_summary(rules_checked)
    ai_insights_summary = generate_ai_insights(rules_checked)
    eligibility = determine_eligibility(drivers, vehicles)

    underwriting = build_underwriting_details(
        drivers,
        vehicles,
        risk_score,
        base_premium,
    )

    ai_insights = build_ai_insights(customer, coverage, risk_score)

    summary = build_summary_block(
        customer,
        drivers,
        vehicles,
        risk_score,
        base_premium,
        eligibility,
    )

    # -----------------------------
    # Unified Final Risk Score
    # -----------------------------
    underwriting_score = risk_score
    rule_score = underwriting_summary.get("riskScore", 100)

    ai_confidence_raw = ai_insights_summary.get("confidence", "0%")
    try:
        ai_confidence_percent = float(str(ai_confidence_raw).replace("%", "").strip())
    except ValueError:
        ai_confidence_percent = 0.0

    final_score = calculate_final_risk_score(
        underwriting_score,
        rule_score,
        ai_confidence_percent,
    )

    final_tier = determine_final_tier(final_score)
    final_decision_flag = determine_final_decision(final_score)

    final_decision = {
        "riskScore": round(final_score, 2),
        "tier": final_tier,
        "decision": final_decision_flag,
        "components": {
            "underwritingScore": underwriting_score,
            "ruleScore": rule_score,
            "aiConfidencePercent": ai_confidence_percent,
        },
    }

    # -----------------------------
    # CLEAN RESPONSE: ONE RISK SCORE
    # -----------------------------
    executive_summary = {
        "riskScore": round(final_score, 2),
        "eligibility": eligibility,
        "basePremium": base_premium,
    }

    summary["riskScore"] = round(final_score, 2)
    if underwriting.get("vehicles"):
        underwriting["vehicles"][0]["riskScore"] = round(final_score, 2)

    underwriting_summary["riskScore"] = round(final_score, 2)

    state_compliance, compliance = build_compliance_block(
        state,
        compliance_meta,
        rules_checked,
        customer_raw,
        vehicles_raw,
        drivers_raw,
        coverage_raw,
        guidewire_raw,
    )

    processed_data = {
        "customer": customer,
        "coverage": coverage,
        "vehicles": vehicles,
        "drivers": drivers,
        "guidewire": guidewire,
        "underwriting": underwriting,
        "aiInsights": ai_insights,
        "summary": summary,
        "executiveSummary": executive_summary,
        "compliance": compliance,
        "stateCompliance": state_compliance,
        "underwritingSummary": underwriting_summary,
        "aiInsightsSummary": ai_insights_summary,
        "finalDecision": final_decision,
    }

    return {"status": "processed", "processed_data": processed_data}


class UnderwriterInput(BaseModel):
    data: dict


@router.post("/receive")
def receive_input(payload: UnderwriterInput):
    processed = process_data(payload.data)
    final_output = dispatch_output(processed)
    return final_output


@router.post("/generate-compliance-report")
def generate_compliance_report(payload: dict):
    processed = payload.get("processed_data", {})

    state_compliance = processed.get("stateCompliance", {})
    underwriting = processed.get("underwriting", {})
    ai_insights = processed.get("aiInsights", {})

    rulesChecked = state_compliance.get("rulesChecked", [])

    for rule in rulesChecked:
        if "passed" not in rule:
            rule["passed"] = True

    summary_obj = ComplianceSummary(
        state=state_compliance.get("state"),
        stateFullName=state_compliance.get("stateFullName"),
        overallComplianceStatus=state_compliance.get("overallComplianceStatus"),
        rulesChecked=rulesChecked,
        complianceSummary=state_compliance.get("notes", ""),
        underwritingSummary=underwriting,
        aiInsightsSummary=ai_insights,
    )

    summary_dict = summary_obj.model_dump()

    # Generate the ReportLab PDF
    output_path = "test_placeholder.pdf"
    generate_pdf(output_path)

    # Read the PDF bytes correctly
    with open(output_path, "rb") as f:
        pdf_bytes = f.read()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=compliance_report.pdf"
        },
    )

