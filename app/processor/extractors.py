# -----------------------------
# Extraction Handlers (Step 2.2)
# -----------------------------

def handle_customer(customer):
    return {
        "firstName": customer.get("firstName"),
        "lastName": customer.get("lastName"),
        "age": customer.get("age"),
        "licenseNumber": customer.get("licenseNumber"),
        "raw": customer
    }


def handle_vehicle(vehicle):
    return {
        "vin": vehicle.get("vin"),
        "year": vehicle.get("year"),
        "make": vehicle.get("make"),
        "model": vehicle.get("model"),
        "raw": vehicle
    }


# ---------- MULTI‑DRIVER (NEW) ----------
def handle_driver(driver):
    return {
        "driverId": driver.get("driverId"),
        "firstName": driver.get("firstName"),
        "lastName": driver.get("lastName"),
        "age": driver.get("age"),
        "licenseStatus": driver.get("licenseStatus"),
        "assignedVehicles": driver.get("assignedVehicles", []),
        "raw": driver
    }
# ----------------------------------------

def handle_coverage(coverage):
    return {
        "liabilityLimit": coverage.get("liabilityLimit"),
        "deductible": coverage.get("deductible"),
        "coverageType": coverage.get("coverageType"),
        "raw": coverage
    }


def handle_guidewire(guidewire):
    return {
        "transactionId": guidewire.get("transactionId"),
        "timestamp": guidewire.get("timestamp"),
        "sourceSystem": guidewire.get("sourceSystem"),
        "state": guidewire.get("state"),
        "raw": guidewire
    }
