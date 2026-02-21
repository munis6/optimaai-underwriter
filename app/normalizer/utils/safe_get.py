def safe_get(obj, path):
    """
    Safely walk a dotted path inside a JSON object.
    If anything is missing, return None instead of crashing.
    """
    if obj is None:
        return None

    parts = path.split(".")
    current = obj

    for part in parts:
        if not isinstance(current, dict):
            return None
        if part not in current:
            return None
        current = current[part]

    return current
