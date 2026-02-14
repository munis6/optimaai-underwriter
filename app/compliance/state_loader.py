# app/compliance/state_loader.py

# This file loads the correct state rules file (like FL.py or AK.py) based on the normalized state code.

import importlib

def load_state_rules(state_code: str):
    """
    Dynamically loads the state rules module (e.g., FL.py, AK.py).
    Returns {} if the module doesn't exist or fails to load.
    """
    if not state_code:
        return {}

    try:
        module_path = f"app.compliance.states.{state_code}"
        module = importlib.import_module(module_path)

        # FL.py uses RULES
        if hasattr(module, "RULES"):
            return {"RULES": getattr(module, "RULES")}

        # All other states use STATE_RULES
        if hasattr(module, "STATE_RULES"):
            return getattr(module, "STATE_RULES")

        return {}

    except Exception:
        return {}
