# app/processor/processor.py
from app.services.underwriting_engine import (
    generate_underwriting_summary,
    generate_ai_insights
)
from .underwriting_engine import run_underwriting

from .extractors import (
    handle_customer,
    handle_vehicle,
    handle_driver,
    handle_coverage,
    handle_guidewire
)
from .decision_builder import build_decision_json

def process_data(payload):
    """
    Step 4.0:
    - Extract fields (Step 2.2)
    - Run underwriting logic (Step 2.3)
    - Build final OptimaAI decision JSON with AI insights (Step 4.0)
    """

    customer = payload.get("customer", {})
    vehicles = payload.get("vehicles", [])      # <-- MULTI‑VEHICLE
    drivers = payload.get("drivers", [])        # <-- MULTI‑DRIVER
    coverage = payload.get("coverage", {})
    guidewire = payload.get("guidewire", {})

    # NEW — Iowa surcharge rule + future states
    previous_premium = payload.get("previousPremium")
    current_premium = payload.get("currentPremium")
    accidents = payload.get("accidents", [])

    # -----------------------------
    # Step 2.2 extraction
    # -----------------------------
    _customer_info = handle_customer(customer)
    _vehicle_info_list = [handle_vehicle(v) for v in vehicles]   # <-- MULTI‑VEHICLE
    _driver_info_list = [handle_driver(d) for d in drivers]      # <-- MULTI‑DRIVER
    _coverage_info = handle_coverage(coverage)
    _guidewire_info = handle_guidewire(guidewire)

    extracted = {
        "customer": _customer_info,
        "vehicles": _vehicle_info_list,        # <-- MULTI‑VEHICLE
        "drivers": _driver_info_list,          # <-- MULTI‑DRIVER
        "coverage": _coverage_info,
        "guidewire": _guidewire_info,
        "state": _guidewire_info.get("state"),

        # Documents + prior insurance
        "documents": payload.get("documents", []),
        "hadPriorInsurance": payload.get("hadPriorInsurance", None),

        # NEW — Required for Iowa rule IA‑RATING‑03
        "previousPremium": previous_premium,
        "currentPremium": current_premium,
        "accidents": accidents
    }
    underwriting = run_underwriting(customer, vehicles, coverage, drivers)

    # -----------------------------
    # Step 4.0: final decision JSON with AI insights
    # -----------------------------
    final_decision = build_decision_json(extracted, underwriting)
    return final_decision

