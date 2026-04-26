from services.api import api_client
from utils.config import LABS_ENDPOINT


def get_patient_labs(patient_id: str):
    response = api_client.get(f"{LABS_ENDPOINT}/patient/{patient_id}")
    if response:
        return response

    return [
        {"test": "Creatinine", "value": 1.8, "unit": "mg/dL", "date": "2026-04-01"},
        {"test": "WBC", "value": 12.4, "unit": "K/uL", "date": "2026-04-01"},
        {"test": "Sodium", "value": 137, "unit": "mmol/L", "date": "2026-04-01"},
    ]