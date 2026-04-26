from pydantic import BaseModel


class AlertItem(BaseModel):
    type: str
    title: str
    message: str
    source: str


class PatientAlertResponse(BaseModel):
    patient_id: int
    has_alerts: bool
    severity: str
    alerts: list[AlertItem]
    review_recommended: bool
    review_reason: str | None = None