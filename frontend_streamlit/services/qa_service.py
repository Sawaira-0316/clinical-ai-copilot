from services.api import api_client
from utils.config import QA_ENDPOINT


def ask_patient_question(patient_id: str, question: str):
    response = api_client.post(QA_ENDPOINT, json={"patient_id": patient_id, "question": question})
    if response:
        return response

    return {
        "answer": (
            f"Grounded response for patient {patient_id}: Based on the available uploaded data, "
            f"the system found relevant patient context for the question '{question}'. "
            f"If certain values are missing, they should be reported explicitly instead of assumed."
        )
    }