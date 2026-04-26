from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.services.clinical.patient_qa_service import PatientQAService

router = APIRouter(prefix="/qa", tags=["Patient Q&A"])


class QARequest(BaseModel):
    patient_id: int
    question: str


@router.post("/ask")
def ask_patient_question(
    payload: QARequest,
    db: Session = Depends(get_db),
):
    return PatientQAService.ask_question(payload.patient_id, payload.question, db)
