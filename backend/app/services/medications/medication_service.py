from sqlalchemy.orm import Session
from app.db.repositories.medication_repository import MedicationRepository
from app.db.repositories.patient_repository import PatientRepository


class MedicationService:
    @staticmethod
    def create_medication(db: Session, data: dict):
        patient = PatientRepository.get_by_id(db, data["patient_id"])
        if not patient:
            raise ValueError(f"Patient {data['patient_id']} not found.")
        return MedicationRepository.create(db, data)

    @staticmethod
    def get_patient_medications(db: Session, patient_id: int):
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError(f"Patient {patient_id} not found.")
        return MedicationRepository.get_by_patient_id(db, patient_id)