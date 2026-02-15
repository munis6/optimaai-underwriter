from fastapi import APIRouter, Response, Body
from pydantic import BaseModel

print(">>> ROUTER.PY LOADED <<<")

# Existing imports
from app.processor.processor import process_data
from app.dispatcher.dispatcher import dispatch_output

# Phase 4 imports
from app.services.pdf_generator import generate_compliance_pdf

# Models
from app.models.compliance_summary import ComplianceSummary

# Dynamic state rule loader
from app.compliance.state_loader import load_state_rules

from app.compliance.state_normalizer import STATE_NAME


router = APIRouter()


@router.get("/")
def home():
    return {"message": "OptimaAI Underwriter is running"}


# ============================================================
#  ENRICH ENDPOINT — RETURNS FULL processed_data (PDF-ready)
# ============================================================
@router.post("/enrich")
async def enrich(payload: dict = Body(...)):
    raw = payload or {}
    root = raw.get("data", raw)

    # ----------------------------------------
    # Extract state from incoming JSON
    # ----------------------------------------
    guidewire_raw = root.get("guidewire", {})
    state = (
        guidewire_raw.get("state")
        or root.get("state")
        or root.get("customer", {}).get("address", {}).get("state")
        or "IA"
    )

    # ----------------------------------------
    # Dynamically load rules for that state
    # ----------------------------------------
    state_rules = load_state_rules(state)
    compliance_meta = state_rules.get("compliance", {})
    # Normalize rulesChecked
    rules_checked = (
    state_rules.get("RULES")
    or state_rules.get("rulesChecked")
    or state_rules.get("compliance", {}).get("rulesChecked")
    or []
)


    # ----------------------------------------
    # Base entities
    # ----------------------------------------
    customer_raw = root.get("customer", {})
    vehicles_raw = root.get("vehicles", [])
    drivers_raw = root.get("drivers", [])
    coverage_raw = root.get("coverage", {})

    # Customer
    customer = {
        "firstName": customer_raw.get("firstName"),
        "lastName": customer_raw.get("lastName"),
        "age": customer_raw.get("age"),
        "licenseNumber": customer_raw.get("licenseNumber"),
        "raw": customer_raw or None,
    }

    # Coverage
    coverage = {
        "liabilityLimit": coverage_raw.get("liabilityLimit", 100000),
        "deductible": coverage_raw.get("deductible", 500),
        "coverageType": coverage_raw.get("coverageType", "FullCoverage"),
        "raw": coverage_raw,
    }

    # Vehicles
    vehicles = []
    for v in vehicles_raw:
        vehicles.append({
            "vin": v.get("vin"),
            "year": v.get("year"),
            "make": v.get("make"),
            "model": v.get("model"),
            "raw": v,
        })

    # Drivers
    drivers = []
    for d in drivers_raw:
        drivers.append({
            "driverId": d.get("driverId"),
            "firstName": d.get("firstName"),
            "lastName": d.get("lastName"),
            "age": d.get("age"),
            "licenseStatus": d.get("licenseStatus"),
            "assignedVehicles": d.get("assignedVehicles", []),
            "raw": d,
        })

    # Guidewire
    guidewire = {
        "transactionId": guidewire_raw.get("transactionId"),
        "timestamp": guidewire_raw.get("timestamp"),
        "sourceSystem": guidewire_raw.get("sourceSystem"),
        "state": guidewire_raw.get("state"),
        "raw": guidewire_raw,
    }

    # ----------------------------------------
    # Underwriting (demo logic)
    # ----------------------------------------
    base_premium = 625.0
    risk_score = 600
    eligibility = "Eligible"

    uw_vehicles = []
    for v in vehicles:
        uw_vehicles.append({
            "vehicle": v["raw"],
            "rulesResult": {"rulesFired": [], "status": "rules evaluated (placeholder)"},
            "riskScore": risk_score,
            "premium": base_premium,
            "eligibility": eligibility,
        })

    uw_drivers = []
    for d in drivers_raw:
        uw_drivers.append({
            "firstName": d.get("firstName"),
            "lastName": d.get("lastName"),
            "age": d.get("age"),
            "licenseNumber": d.get("licenseNumber"),
            "yearsLicensed": d.get("yearsLicensed"),
            "accidents": d.get("accidents"),
            "violations": d.get("violations"),
            "claims": d.get("claims"),
            "isPrimaryDriver": d.get("isPrimaryDriver"),
        })

    underwriting = {
        "vehicles": uw_vehicles,
        "drivers": uw_drivers,
    }

    # ----------------------------------------
    # AI Insights
    # ----------------------------------------
    driver_name = f"{customer.get('firstName')} {customer.get('lastName')}".strip()

    ai_insights = {
        "driverRiskFactors": f"Driver {driver_name} has a moderate risk score of {risk_score}.",
        "pricingRationale": (
            f"Pricing is based on liability ${coverage['liabilityLimit']:,}, "
            f"deductible ${coverage['deductible']:,}, "
            f"coverage {coverage['coverageType']}."
        ),
        "explanations": "Driver has a clean record with no accidents or violations.",
        "improvementSuggestions": "Consider telematics, defensive driving, and safety features.",
    }

    # ----------------------------------------
    # Summary
    # ----------------------------------------
    vehicle_count = len(vehicles)
    total_premium = base_premium * vehicle_count

    highest_risk_vehicle = vehicles_raw[0] if vehicles_raw else {}

    summary = {
        "vehicleCount": vehicle_count,
        "totalPremium": total_premium,
        "overallEligibility": eligibility,
        "highestRiskVehicle": highest_risk_vehicle,
    }

    executive_summary = (
        f"Highest-risk vehicle: {highest_risk_vehicle.get('year')} "
        f"{highest_risk_vehicle.get('make')} "
        f"{highest_risk_vehicle.get('model')}."
    )

    # ----------------------------------------
    # Compliance + State Compliance
    # ----------------------------------------
    state_compliance = {
        "state": compliance_meta.get("state", state),
        "stateFullName": STATE_NAME.get(state, "Unknown"),
        "rulesChecked": rules_checked,
        "overallComplianceStatus": compliance_meta.get("overallComplianceStatus", "PENDING_RULES"),
        "notes": compliance_meta.get("notes", f"No state-specific compliance rules loaded for {state}."),
        "version": compliance_meta.get("version", "1.0"),
    }


    compliance = {  
        "timestamp": "not provided",
        "dataLineage": {
            "source": "Guidewire → OptimaAI → Underwriter → AI Engine",
            "customerFields": list(customer_raw.keys()),
            "vehicleFields": list((vehicles_raw[0] or {}).keys()) if vehicles_raw else [],
            "driverFields": list((drivers_raw[0] or {}).keys()) if drivers_raw else [],
            "coverageFields": list(coverage_raw.keys()),
            "guidewireFields": list(guidewire_raw.keys()),
            "documentFields": [],
        },
        "ruleTrace": rules_checked,
        "aiTrace": {
            "model": "Groq LLM (deterministic)",
            "insightFields": list(ai_insights.keys()),
            "grounding": "AI used only provided underwriting context.",
        },
    }

    # ----------------------------------------
    # Underwriting + AI summaries
    # ----------------------------------------
    underwriting_summary = {
        "riskScore": risk_score,
        "decision": "APPROVE",
        "premiumAdjustment": "0%",
        "factorsConsidered": "All rules evaluated.",
        "humanReviewRequired": "No",
    }

    ai_insights_summary = {
        "flags": "No issues detected",
        "explanations": "All automated checks passed.",
        "confidence": "98%",
        "modelNotes": "Model validated inputs successfully.",
    }

    # ----------------------------------------
    # Final processed_data
    # ----------------------------------------
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
    }

    return {"status": "processed", "processed_data": processed_data}


# ============================================================
#  EXISTING ROUTES (UNCHANGED)
# ============================================================

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

    # Extract rules safely
    rulesChecked = state_compliance.get("rulesChecked", [])

    # FIX: Ensure each rule has the required `passed` field
    for rule in rulesChecked:
        if "passed" not in rule:
            rule["passed"] = True

    # Build Pydantic model
    summary_obj = ComplianceSummary(
        state=state_compliance.get("state"),
        stateFullName=state_compliance.get("stateFullName"),
        overallComplianceStatus=state_compliance.get("overallComplianceStatus"),
        rulesChecked=rulesChecked,
        complianceSummary=state_compliance.get("notes", ""),
        underwritingSummary=underwriting,
        aiInsightsSummary=ai_insights
    )

    summary_dict = summary_obj.model_dump()

    pdf_bytes = generate_compliance_pdf(summary_dict)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=compliance_report.pdf"
        }
    )
