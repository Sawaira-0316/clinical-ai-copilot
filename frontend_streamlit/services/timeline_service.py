from services.api import api_client
from utils.config import TIMELINE_ENDPOINT


def get_patient_timeline(patient_id: str):
    response = api_client.get(f"{TIMELINE_ENDPOINT}/{patient_id}")
    if response:
        return response

    return [
        {"time": "2026-04-01 08:00", "event": "Admission", "details": "Patient admitted for review"},
        {"time": "2026-04-01 10:00", "event": "Vitals Recorded", "details": "HR 96, Temp 37.8"},
        {"time": "2026-04-01 12:00", "event": "Medication", "details": "Paracetamol 500mg"},
        {"time": "2026-04-01 15:00", "event": "Lab Result", "details": "Creatinine elevated"},
    ]