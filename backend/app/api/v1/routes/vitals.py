from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.vital_sign import VitalSignCreate, VitalSignResponse
from app.db.session import get_db
from app.services.vitals.vital_sign_service import VitalSignService

router = APIRouter()


@router.post("/vitals", response_model=VitalSignResponse, tags=["Vitals"])
def create_vital_sign(
    payload: VitalSignCreate,
    db: Session = Depends(get_db),
):
    try:
        return VitalSignService.create_vital_sign(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create vital sign: {str(exc)}")


@router.get("/vitals/patient/{patient_id}", response_model=list[VitalSignResponse], tags=["Vitals"])
def get_patient_vitals(
    patient_id: int,
    db: Session = Depends(get_db),
):
    try:
        return VitalSignService.get_patient_vitals(db, patient_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch vital signs: {str(exc)}")