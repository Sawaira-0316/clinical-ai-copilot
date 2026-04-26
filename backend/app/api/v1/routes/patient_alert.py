from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.patient_alert import PatientAlertResponse
from app.db.session import get_db
from app.services.clinical.patient_alert_service import PatientAlertService

router = APIRouter()


@router.get("/patients/{patient_id}/alerts", response_model=PatientAlertResponse, tags=["Patient Alerts"])
def get_patient_alerts(
    patient_id: int,
    db: Session = Depends(get_db),
):
    try:
        return PatientAlertService.get_patient_alerts(db, patient_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch patient alerts: {str(exc)}")