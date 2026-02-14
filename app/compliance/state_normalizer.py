# app/compliance/state_normalizer.py

# This file converts any incoming state value (like "Florida" or "FL") into a clean 2‑letter state code.

STATE_MAP = {
        "alabama": "AL", "al": "AL",
        "alaska": "AK", "ak": "AK",
        "arizona": "AZ", "az": "AZ",
        "arkansas": "AR", "ar": "AR",
        "california": "CA", "ca": "CA",
        "colorado": "CO", "co": "CO",
        "connecticut": "CT", "ct": "CT",
        "delaware": "DE", "de": "DE",
        "florida": "FL", "fl": "FL",
        "georgia": "GA", "ga": "GA",
        "hawaii": "HI", "hi": "HI",
        "idaho": "ID", "id": "ID",
        "illinois": "IL", "il": "IL",
        "indiana": "IN", "in": "IN",
        "iowa": "IA", "ia": "IA",
        "kansas": "KS", "ks": "KS",
        "kentucky": "KY", "ky": "KY",
        "louisiana": "LA", "la": "LA",
        "maine": "ME", "me": "ME",
        "maryland": "MD", "md": "MD",
        "massachusetts": "MA", "ma": "MA",
        "michigan": "MI", "mi": "MI",
        "minnesota": "MN", "mn": "MN",
        "mississippi": "MS", "ms": "MS",
        "missouri": "MO", "mo": "MO",
        "montana": "MT", "mt": "MT",
        "nebraska": "NE", "ne": "NE",
        "nevada": "NV", "nv": "NV",
        "new hampshire": "NH", "nh": "NH",
        "new jersey": "NJ", "nj": "NJ",
        "new mexico": "NM", "nm": "NM",
        "new york": "NY", "ny": "NY",
        "north carolina": "NC", "nc": "NC",
        "north dakota": "ND", "nd": "ND",
        "ohio": "OH", "oh": "OH",
        "oklahoma": "OK", "ok": "OK",
        "oregon": "OR", "or": "OR",
        "pennsylvania": "PA", "pa": "PA",
        "rhode island": "RI", "ri": "RI",
        "south carolina": "SC", "sc": "SC",
        "south dakota": "SD", "sd": "SD",
        "tennessee": "TN", "tn": "TN",
        "texas": "TX", "tx": "TX",
        "utah": "UT", "ut": "UT",
        "vermont": "VT", "vt": "VT",
        "virginia": "VA", "va": "VA",
        "washington": "WA", "wa": "WA",
        "west virginia": "WV", "wv": "WV",
        "wisconsin": "WI", "wi": "WI",
        "wyoming": "WY", "wy": "WY"
}
STATE_NAME = {code: name.title() for name, code in STATE_MAP.items() if len(name) > 2}
def normalize_state(value: str) -> str:
    if not value:
        return None
    key = value.strip().lower()
    return STATE_MAP.get(key)
