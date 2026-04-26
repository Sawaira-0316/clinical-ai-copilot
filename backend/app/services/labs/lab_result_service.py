from sqlalchemy.orm import Session
from app.db.repositories.lab_result_repository import LabResultRepository
from app.db.repositories.patient_repository import PatientRepository


class LabResultService:
    @staticmethod
    def create_lab_result(db: Session, data: dict):
        patient = PatientRepository.get_by_id(db, data["patient_id"])
        if not patient:
            raise ValueError(f"Patient {data['patient_id']} not found.")
        return LabResultRepository.create(db, data)

    @staticmethod
    def get_patient_labs(db: Session, patient_id: int):
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError(f"Patient {patient_id} not found.")
        return LabResultRepository.get_by_patient_id(db, patient_id)