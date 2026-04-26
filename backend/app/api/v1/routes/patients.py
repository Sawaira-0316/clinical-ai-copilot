from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.patient import PatientCreate, PatientResponse
from app.api.v1.schemas.patient_context import PatientContextResponse
from app.db.session import get_db
from app.services.clinical.patient_service import PatientService
from app.services.patients.patient_context_service import PatientContextService

router = APIRouter()


@router.post("/patients", response_model=PatientResponse, tags=["Patients"])
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    return PatientService.create_patient(db, payload.model_dump())


@router.get("/patients", response_model=list[PatientResponse], tags=["Patients"])
def get_patients(db: Session = Depends(get_db)):
    return PatientService.get_patients(db)


@router.get("/patients/{patient_id}", response_model=PatientResponse, tags=["Patients"])
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = PatientService.get_patient(db, patient_id)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


@router.get("/patients/{patient_id}/context", response_model=PatientContextResponse, tags=["Patients"])
def get_patient_context(
    patient_id: int,
    db: Session = Depends(get_db),
):
    try:
        return PatientContextService.get_patient_context(db, patient_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch patient context: {str(exc)}")