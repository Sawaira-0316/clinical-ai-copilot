from datetime import datetime

from pydantic import BaseModel


class ClinicalNoteCreate(BaseModel):
    patient_id: int
    note_type: str
    title: str
    content: str
    note_time: datetime


class ClinicalNoteResponse(BaseModel):
    id: int
    patient_id: int
    note_type: str
    title: str
    content: str
    note_time: datetime

    class Config:
        from_attributes = True