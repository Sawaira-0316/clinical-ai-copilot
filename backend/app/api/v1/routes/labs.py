from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.lab_result import LabResultCreate, LabResultResponse
from app.db.session import get_db
from app.services.labs.lab_result_service import LabResultService

router = APIRouter()


@router.post("/labs", response_model=LabResultResponse, tags=["Labs"])
def create_lab_result(
    payload: LabResultCreate,
    db: Session = Depends(get_db),
):
    try:
        return LabResultService.create_lab_result(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create lab result: {str(exc)}")


@router.get("/labs/patient/{patient_id}", response_model=list[LabResultResponse], tags=["Labs"])
def get_patient_labs(
    patient_id: int,
    db: Session = Depends(get_db),
):
    try:
        return LabResultService.get_patient_labs(db, patient_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lab results: {str(exc)}")