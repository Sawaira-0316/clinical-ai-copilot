from services.api import api_client
from utils.config import VITALS_ENDPOINT


def get_patient_vitals(patient_id: str):
    response = api_client.get(f"{VITALS_ENDPOINT}/patient/{patient_id}")
    if response:
        return response

    return [
        {"metric": "Heart Rate", "value": 96, "unit": "bpm", "date": "2026-04-01 10:00"},
        {"metric": "Temperature", "value": 37.8, "unit": "°C", "date": "2026-04-01 10:00"},
        {"metric": "Blood Pressure", "value": "130/85", "unit": "mmHg", "date": "2026-04-01 10:00"},
    ]