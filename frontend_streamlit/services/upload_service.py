import requests
from utils.config import UPLOADS_ENDPOINT


def upload_patient_dataset(uploaded_file, filename=None):
    files = {
        "file": (
            filename or uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "application/octet-stream",
        )
    }
    response = requests.post(UPLOADS_ENDPOINT, files=files, timeout=120)
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json()

import requests
from utils.config import UPLOADS_ENDPOINT


def upload_patient_dataset(uploaded_file, filename=None):
    files = {
        "file": (
            filename or uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "application/octet-stream",
        )
    }
    response = requests.post(UPLOADS_ENDPOINT, files=files, timeout=120)
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json()