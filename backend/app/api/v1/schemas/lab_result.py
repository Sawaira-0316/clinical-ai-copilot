from datetime import datetime
from pydantic import BaseModel


class LabResultCreate(BaseModel):
    patient_id: int
    lab_name: str
    value: float
    unit: str | None = None
    reference_range: str | None = None
    is_abnormal: bool = False
    measured_at: datetime


class LabResultResponse(BaseModel):
    id: int
    patient_id: int
    lab_name: str
    value: float
    unit: str | None = None
    reference_range: str | None = None
    is_abnormal: bool
    measured_at: datetime

    class Config:
        from_attributes = True