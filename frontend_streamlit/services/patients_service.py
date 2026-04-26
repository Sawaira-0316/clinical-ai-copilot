from services.api import api_client
from utils.config import PATIENTS_ENDPOINT


def get_patients(search: str = ""):
    response = api_client.get(PATIENTS_ENDPOINT, params={"search": search} if search else None)
    if response:
        # Backend returns list of patients with id, name, age, gender
        return [
            {
                "patient_id": str(p.get("id", "")),
                "name": p.get("name", "Unknown"),
                "gender": p.get("gender", "N/A"),
                "age": p.get("age", "N/A"),
                "status": "Stable",
            }
            for p in response
        ]
    # Fallback mock data if backend is down
    return [
        {"patient_id": "P001", "name": "Muhammad Ali", "gender": "Male", "age": 54, "status": "Stable"},
        {"patient_id": "P002", "name": "Sara Khan", "gender": "Female", "age": 39, "status": "Warning"},
        {"patient_id": "P003", "name": "Ahmed Raza", "gender": "Male", "age": 65, "status": "Critical"},
    ]


def get_patient_by_id(patient_id: str):
    response = api_client.get(f"{PATIENTS_ENDPOINT}/{patient_id}")
    if response:
        return {
            "patient_id": str(response.get("id", "")),
            "name": response.get("name", "Unknown"),
            "gender": response.get("gender", "N/A"),
            "age": response.get("age", "N/A"),
            "status": "Stable",
        }
    # Fallback — search in full list
    patients = get_patients()
    for patient in patients:
        if patient["patient_id"] == patient_id:
            return patient
    return None
