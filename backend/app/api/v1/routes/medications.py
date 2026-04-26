from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.medication import MedicationCreate, MedicationResponse
from app.db.session import get_db
from app.services.medications.medication_service import MedicationService

router = APIRouter()


@router.post("/medications", response_model=MedicationResponse, tags=["Medications"])
def create_medication(
    payload: MedicationCreate,
    db: Session = Depends(get_db),
):
    try:
        return MedicationService.create_medication(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create medication: {str(exc)}")


@router.get("/medications/patient/{patient_id}", response_model=list[MedicationResponse], tags=["Medications"])
def get_patient_medications(
    patient_id: int,
    db: Session = Depends(get_db),
):
    try:
        return MedicationService.get_patient_medications(db, patient_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch medications: {str(exc)}")