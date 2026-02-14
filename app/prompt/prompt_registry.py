# app/prompts/prompt_registry.py

from .simple_prompt import SIMPLE_PROMPT
from .multi_driver_multi_vehicle_prompt import MULTI_DRIVER_MULTI_VEHICLE_PROMPT
from .violations_prompt import VIOLATIONS_PROMPT
from .single_driver_multi_vehicle_prompt import SINGLE_DRIVER_MULTI_VEHICLE_PROMPT
from .multi_driver_single_vehicle_prompt import MULTI_DRIVER_SINGLE_VEHICLE_PROMPT



PROMPT_MAP = {
    "simple": SIMPLE_PROMPT,
    "single_driver_multi_vehicle": SINGLE_DRIVER_MULTI_VEHICLE_PROMPT,
    "multi_driver_multi_vehicle": MULTI_DRIVER_MULTI_VEHICLE_PROMPT,
    "multi_driver_single_vehicle": MULTI_DRIVER_SINGLE_VEHICLE_PROMPT,
    "violations": VIOLATIONS_PROMPT
}


def detect_scenario(underwriting_context: dict) -> str:
    drivers = underwriting_context.get("drivers", [])
    vehicles = underwriting_context.get("vehicles", [])

    has_multiple_drivers = len(drivers) > 1
    has_multiple_vehicles = len(vehicles) > 1
    has_violations = any(d.get("violations") for d in drivers)

    # 1) Violations always override everything
    if has_violations:
        return "violations"

    # 2) Multi‑driver + multi‑vehicle
    if has_multiple_drivers and has_multiple_vehicles:
        return "multi_driver_multi_vehicle"

    # 3) Single driver + multiple vehicles
    if not has_multiple_drivers and has_multiple_vehicles:
        return "single_driver_multi_vehicle"
    
    # 4) Multiple drivers + single vehicle
    if has_multiple_drivers and not has_multiple_vehicles: 
        return "multi_driver_single_vehicle"
    
    # 5) Default fallback
    return "simple"


def get_system_prompt(underwriting_context: dict) -> str:
    scenario = detect_scenario(underwriting_context)
    return PROMPT_MAP.get(scenario, SIMPLE_PROMPT)
