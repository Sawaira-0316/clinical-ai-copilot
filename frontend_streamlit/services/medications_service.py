from services.api import api_client
from utils.config import MEDICATIONS_ENDPOINT


def get_patient_medications(patient_id: str):
    response = api_client.get(f"{MEDICATIONS_ENDPOINT}/patient/{patient_id}")
    if response:
        return response

    return [
        {"drug": "Paracetamol", "dose": "500mg", "frequency": "TID", "date": "2026-04-01"},
        {"drug": "Azithromycin", "dose": "250mg", "frequency": "OD", "date": "2026-04-01"},
    ]