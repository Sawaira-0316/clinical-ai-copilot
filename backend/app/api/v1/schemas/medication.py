from datetime import datetime

from pydantic import BaseModel


class MedicationCreate(BaseModel):
    patient_id: int
    medication_name: str
    dose: str | None = None
    route: str | None = None
    frequency: str | None = None
    status: str = "active"
    indication: str | None = None
    start_time: datetime
    end_time: datetime | None = None
    is_active: bool = True


class MedicationResponse(BaseModel):
    id: int
    patient_id: int
    medication_name: str
    dose: str | None = None
    route: str | None = None
    frequency: str | None = None
    status: str
    indication: str | None = None
    start_time: datetime
    end_time: datetime | None = None
    is_active: bool

    class Config:
        from_attributes = True