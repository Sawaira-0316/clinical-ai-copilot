from services.api import api_client
from utils.config import SUMMARY_ENDPOINT


def get_patient_summary(patient_id: str):
    try:
        pid = int(patient_id)
    except (ValueError, TypeError):
        pid = patient_id
    response = api_client.get(f"{SUMMARY_ENDPOINT}/{pid}/summary")
    if response:
        return response
    return {"summary": "No summary available."}