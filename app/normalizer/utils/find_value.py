from .safe_get import safe_get

def find_value(obj, paths):
    """
    Try multiple possible JSON paths and return the first value found.
    If none exist, return None.
    """
    for path in paths:
        value = safe_get(obj, path)
        if value is not None:
            return value
    return None
