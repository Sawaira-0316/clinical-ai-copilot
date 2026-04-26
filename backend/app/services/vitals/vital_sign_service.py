from sqlalchemy.orm import Session

from app.db.repositories.patient_repository import PatientRepository
from app.db.repositories.vital_sign_repository import VitalSignRepository


class VitalSignService:
    @staticmethod
    def create_vital_sign(db: Session, data: dict):
        patient = PatientRepository.get_by_id(db, data["patient_id"])
        if not patient:
            raise ValueError("Patient not found")

        return VitalSignRepository.create(db, data)

    @staticmethod
    def get_patient_vitals(db: Session, patient_id: int):
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError("Patient not found")

        return VitalSignRepository.get_by_patient_id(db, patient_id)