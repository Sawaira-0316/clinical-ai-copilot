from sqlalchemy.orm import Session
from app.db.repositories.clinical_note_repository import ClinicalNoteRepository
from app.db.repositories.patient_repository import PatientRepository


class ClinicalNoteService:
    @staticmethod
    def create_note(db: Session, data: dict):
        patient = PatientRepository.get_by_id(db, data["patient_id"])
        if not patient:
            raise ValueError(f"Patient {data['patient_id']} not found.")
        return ClinicalNoteRepository.create(db, data)

    @staticmethod
    def get_patient_notes(db: Session, patient_id: int):
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError(f"Patient {patient_id} not found.")
        return ClinicalNoteRepository.get_by_patient_id(db, patient_id)