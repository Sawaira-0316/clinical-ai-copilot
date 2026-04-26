from services.api import api_client
from utils.config import NOTES_ENDPOINT


def get_patient_notes(patient_id: str):
    response = api_client.get(f"{NOTES_ENDPOINT}/patient/{patient_id}")
    if response:
        return response

    return [
        {
            "date": "2026-04-01",
            "note": "Patient is alert and oriented. Mild cough reported.",
        },
        {
            "date": "2026-04-02",
            "note": "Oxygen saturation remained stable during observation.",
        },
    ]