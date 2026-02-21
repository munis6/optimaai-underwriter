import json
from app.normalizer.normalizer import normalize_incoming_json

# Messy insurer JSON
raw_json = {
    "insured": {
        "givenName": "John",
        "familyName": "Doe",
        "location": {
            "postalCode": "50001",
            "stateCd": "IA"
        }
    },
    "operatorList": [
        {
            "fname": "John",
            "lname": "Doe",
            "accHist": 1
        }
    ]
}

normalized = normalize_incoming_json(raw_json)

print(json.dumps(normalized, indent=2))
