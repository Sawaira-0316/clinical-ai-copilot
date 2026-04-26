from sqlalchemy.orm import Session
from app.db.repositories.patient_repository import PatientRepository


class PatientContextService:

    @staticmethod
    def get_patient_context(db: Session, patient_id: int):
        patient = PatientRepository.get_by_id(db, patient_id)

        if not patient:
            return None

        return {
            "id": patient.id,
            "name": getattr(patient, "name", None),
        }