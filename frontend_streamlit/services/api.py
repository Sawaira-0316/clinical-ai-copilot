import requests


class APIClient:
    def __init__(self, timeout=20):
        self.timeout = timeout

    def get(self, url, params=None):
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def post(self, url, json=None, files=None, data=None):
        try:
            response = requests.post(url, json=json, files=files, data=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


api_client = APIClient()