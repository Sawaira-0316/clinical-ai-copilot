from pydantic import BaseModel
from typing import Optional


class PatientSummaryResponse(BaseModel):
    patient_id: int
    summary: str
    generated_at: Optional[str] = None