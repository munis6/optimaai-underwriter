# schema_scanner_agent.py

class SchemaScannerAgent:
    def __init__(self):
        self.name = "SchemaScannerAgent"

    def scan(self, payload: dict) -> dict:
        """
        Step 4: Real schema validation logic.
        This agent checks for required top-level fields,
        identifies missing or empty sections, and prepares
        the data for downstream processors.
        """

        required_fields = [
            "submissionId",
            "applicant",
            "drivers",
            "vehicles",
            "coverages",
            "requestedEffectiveDate",
            "producer"
        ]

        missing_fields = []
        empty_fields = []

        # Check for missing or empty fields
        for field in required_fields:
            if field not in payload:
                missing_fields.append(field)
            else:
                if payload[field] in (None, "", [], {}):
                    empty_fields.append(field)

        # Build normalized structure for downstream agents
        normalized = {
            "submissionId": payload.get("submissionId"),
            "state": payload.get("applicant", {}).get("address", {}).get("state"),
            "driversCount": len(payload.get("drivers", [])),
            "vehiclesCount": len(payload.get("vehicles", [])),
            "hasAccidents": any(d.get("accidents") for d in payload.get("drivers", [])),
            "hasViolations": any(d.get("violations") for d in payload.get("drivers", [])),
        }

        return {
            "status": "schema_scan_complete",
            "missingFields": missing_fields,
            "emptyFields": empty_fields,
            "normalized": normalized,
            "receivedKeys": list(payload.keys())
        }
