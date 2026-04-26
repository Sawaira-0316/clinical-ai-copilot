from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.timeline import TimelineEventCreate, TimelineEventResponse
from app.db.session import get_db
from app.services.timeline.timeline_service import TimelineService

router = APIRouter()


@router.post("/timeline/events", response_model=TimelineEventResponse, tags=["Timeline"])
def create_timeline_event(
    payload: TimelineEventCreate,
    db: Session = Depends(get_db),
):
    try:
        return TimelineService.create_event(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(exc)}")


@router.get("/timeline/{patient_id}", response_model=list[TimelineEventResponse], tags=["Timeline"])
def get_patient_timeline(
    patient_id: int,
    db: Session = Depends(get_db),
):
    try:
        return TimelineService.get_patient_timeline(db, patient_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch timeline: {str(exc)}")