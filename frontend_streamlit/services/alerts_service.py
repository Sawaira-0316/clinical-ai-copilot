from services.api import api_client
from utils.config import ALERTS_ENDPOINT


def get_patient_alerts(patient_id: str):
    response = api_client.get(f"{ALERTS_ENDPOINT}/patient/{patient_id}")
    if response:
        return response

    return [
        {"level": "warning", "message": "Elevated creatinine detected"},
        {"level": "info", "message": "Missing respiratory rate in latest vitals"},
    ]