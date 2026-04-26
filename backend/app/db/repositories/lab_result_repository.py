from sqlalchemy.orm import Session
from app.db.models.lab_result import LabResult


class LabResultRepository:
    @staticmethod
    def create(db: Session, data: dict) -> LabResult:
        lab = LabResult(**data)
        db.add(lab)
        db.commit()
        db.refresh(lab)
        return lab

    @staticmethod
    def get_by_patient_id(db: Session, patient_id: int):
        return (
            db.query(LabResult)
            .filter(LabResult.patient_id == patient_id)
            .order_by(LabResult.measured_at.asc())
            .all()
        )