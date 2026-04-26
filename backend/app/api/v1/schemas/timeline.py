from datetime import datetime

from pydantic import BaseModel


class TimelineEventCreate(BaseModel):
    patient_id: int
    event_type: str
    title: str
    description: str | None = None
    event_time: datetime


class TimelineEventResponse(BaseModel):
    id: int
    patient_id: int
    event_type: str
    title: str
    description: str | None = None
    event_time: datetime

    class Config:
        from_attributes = True