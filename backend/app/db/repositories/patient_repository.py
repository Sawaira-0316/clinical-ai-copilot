
from sqlalchemy.orm import Session
from app.db.models.patient import Patient


class PatientRepository:
    @staticmethod
    def create(db: Session, data: dict) -> Patient:
        patient = Patient(**data)
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def create_many(db: Session, items: list) -> list:
        patients = [Patient(**item) for item in items]
        db.add_all(patients)
        db.commit()
        for p in patients:
            db.refresh(p)
        return patients

    @staticmethod
    def get_all(db: Session) -> list:
        return db.query(Patient).all()

    @staticmethod
    def get_by_id(db: Session, patient_id: int):
        return db.query(Patient).filter(Patient.id == patient_id).first()
