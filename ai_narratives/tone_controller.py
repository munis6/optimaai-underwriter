# tone_controller.py

import re

def apply_tone_control(text: str) -> str:
    """
    Ensures all narratives follow a consistent, professional,
    regulator-safe tone and formatting.
    """

    if not text:
        return ""

    # Remove double spaces
    text = re.sub(r"\s{2,}", " ", text)

    # Ensure consistent sentence spacing
    text = re.sub(r"\.\s*", ". ", text)

    # Remove trailing spaces
    text = text.strip()

    # Ensure the narrative ends with a period
    if not text.endswith("."):
        text += "."

    # Replace hype or risky language
    replacements = {
        "guarantee": "indicate",
        "definitely": "clearly",
        "certainly": "generally",
        "always": "typically",
        "never": "generally not",
        "perfect": "appropriate",
        "best": "suitable",
        "worst": "less favorable",
        "safe": "appropriate",
        "unsafe": "less appropriate",
    }

    for word, replacement in replacements.items():
        text = re.sub(rf"\b{word}\b", replacement, text, flags=re.IGNORECASE)

    return text
