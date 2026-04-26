from pydantic import BaseModel

from app.api.v1.schemas.patient import PatientResponse
from app.api.v1.schemas.timeline import TimelineEventResponse
from app.api.v1.schemas.clinical_note import ClinicalNoteResponse
from app.api.v1.schemas.lab_result import LabResultResponse
from app.api.v1.schemas.vital_sign import VitalSignResponse
from app.api.v1.schemas.medication import MedicationResponse


class PatientContextResponse(BaseModel):
    patient: PatientResponse
    timeline: list[TimelineEventResponse]
    notes: list[ClinicalNoteResponse]
    labs: list[LabResultResponse]
    vitals: list[VitalSignResponse]
    medications: list[MedicationResponse]

    class Config:
        from_attributes = True