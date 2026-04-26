from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.schemas.patient_summary import PatientSummaryResponse
from app.db.session import get_db
from app.services.clinical.patient_summary_service import PatientSummaryService

router = APIRouter()


@router.get("/patients/{patient_id}/summary", response_model=PatientSummaryResponse, tags=["Patient Summary"])
def get_patient_summary(
    patient_id: int,
    db: Session = Depends(get_db),
):
    try:
        return PatientSummaryService.get_patient_summary(db, patient_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch patient summary: {str(exc)}")