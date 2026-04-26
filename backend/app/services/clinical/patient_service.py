from sqlalchemy.orm import Session
from app.db.repositories.patient_repository import PatientRepository


class PatientService:

    @staticmethod
    def create_patient(db: Session, data: dict):
        return PatientRepository.create(db, data)

    @staticmethod
    def create_patients_bulk(db: Session, rows: list[dict]):
        if not rows:
            return []
        return PatientRepository.create_many(db, rows)

    @staticmethod
    def get_patients(db: Session):
        return PatientRepository.get_all(db)

    @staticmethod
    def get_patient(db: Session, patient_id: int):
        return PatientRepository.get_by_id(db, patient_id)