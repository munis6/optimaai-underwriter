from .safe_get import safe_get

def find_list(obj, possible_paths):
    """
    Try multiple possible JSON paths and return the first list found.
    If none exist, return an empty list.
    """
    for path in possible_paths:
        value = safe_get(obj, path)
        if isinstance(value, list):
            return value
    return []
