from sqlalchemy.orm import Session

from app.db.models.medication import Medication


class MedicationRepository:
    @staticmethod
    def create(db: Session, data: dict) -> Medication:
        medication = Medication(**data)
        db.add(medication)
        db.commit()
        db.refresh(medication)
        return medication

    @staticmethod
    def get_by_patient_id(db: Session, patient_id: int):
        return (
            db.query(Medication)
            .filter(Medication.patient_id == patient_id)
            .order_by(Medication.start_time.asc())
            .all()
        )