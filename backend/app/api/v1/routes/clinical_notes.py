from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.clinical_note import ClinicalNoteCreate, ClinicalNoteResponse
from app.db.session import get_db
from app.services.notes.clinical_note_service import ClinicalNoteService

router = APIRouter()


@router.post("/notes", response_model=ClinicalNoteResponse, tags=["Clinical Notes"])
def create_clinical_note(
    payload: ClinicalNoteCreate,
    db: Session = Depends(get_db),
):
    try:
        return ClinicalNoteService.create_note(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create clinical note: {str(exc)}")


@router.get("/notes/patient/{patient_id}", response_model=list[ClinicalNoteResponse], tags=["Clinical Notes"])
def get_patient_notes(
    patient_id: int,
    db: Session = Depends(get_db),
):
    try:
        return ClinicalNoteService.get_patient_notes(db, patient_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch clinical notes: {str(exc)}")