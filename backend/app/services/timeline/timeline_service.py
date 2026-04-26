from sqlalchemy.orm import Session
from app.db.repositories.timeline_repository import TimelineRepository
from app.db.repositories.patient_repository import PatientRepository


class TimelineService:
    @staticmethod
    def create_event(db: Session, data: dict):
        patient = PatientRepository.get_by_id(db, data["patient_id"])
        if not patient:
            raise ValueError(f"Patient {data['patient_id']} not found.")
        return TimelineRepository.create(db, data)

    @staticmethod
    def get_patient_timeline(db: Session, patient_id: int):
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError(f"Patient {patient_id} not found.")
        return TimelineRepository.get_by_patient_id(db, patient_id)