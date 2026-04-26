from datetime import datetime
from pydantic import BaseModel


class VitalSignCreate(BaseModel):
    patient_id: int
    vital_name: str
    value: float
    unit: str | None = None
    is_abnormal: bool = False
    measured_at: datetime


class VitalSignResponse(BaseModel):
    id: int
    patient_id: int
    vital_name: str
    value: float
    unit: str | None = None
    is_abnormal: bool
    measured_at: datetime

    class Config:
        from_attributes = True